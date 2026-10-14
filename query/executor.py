"""Execute a validated QuerySpec against the Phase 1 tables. Plain pandas, no LLM involved.

Everything aggregates from player_match.parquet, so stage / opponent filters simply restrict the
matches before summing. A player's position group is always their tournament-wide primary group.
"""
import re
import unicodedata
from difflib import SequenceMatcher
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

from query.describe import describe
from query.schema import METRICS, QuerySpec

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

# Default minutes threshold for rankings where tiny samples would dominate (per-90, rates, and
# "fewest" sorts): 270 over the whole tournament, 90 once stage/opponent filters shrink the sample.
DEFAULT_MIN_MINUTES = 270
DEFAULT_MIN_MINUTES_SUBSET = 90


class ExecutionError(ValueError):
    """The spec is valid but cannot be answered (e.g. an unknown or ambiguous player name)."""


@lru_cache(maxsize=1)
def load_tables():
    pm = pd.read_parquet(DATA_DIR / "player_match.parquet")
    players = pd.read_parquet(DATA_DIR / "players.parquet")
    pm["position_group"] = pm["player_id"].map(players.set_index("player_id")["position_group"])
    return pm, players


# ---------------------------------------------------------------- player names

def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"['’]s\b", "", s)  # possessive: "Ziyech's" -> "Ziyech"
    return " ".join(s.lower().replace("-", " ").replace(".", " ").split())


# Minimum difflib similarity for a "Did you mean" suggestion, and how many to offer.
SUGGEST_CUTOFF = 0.75
MAX_SUGGESTIONS = 3


class NameNotResolved(ExecutionError):
    """A player name matched nobody, or several players. Never guessed: the caller shows a
    "Did you mean ...?" with `suggestions` (display name, team) instead of answering."""

    def __init__(self, name: str, suggestions: list[tuple[str, str]], ambiguous: bool):
        self.name, self.suggestions, self.ambiguous = name, suggestions, ambiguous
        super().__init__(did_you_mean_message(name, suggestions, ambiguous))


def did_you_mean_message(name: str, suggestions: list[tuple[str, str]], ambiguous: bool) -> str:
    options = [f"{p} ({t})" for p, t in suggestions]
    if not options:
        return f"No player matches '{name}'."
    joined = options[0] if len(options) == 1 else ", ".join(options[:-1]) + " or " + options[-1]
    return f"'{name}' could be several players. Did you mean {joined}?" if ambiguous \
        else f"No player matches '{name}'. Did you mean {joined}?"


def _similar(q: str, display: str) -> float:
    """Best difflib ratio of the query against the whole display name or any run of as many of its
    tokens as the query has ("de bruyn" vs "de bruyne", "mbape" vs "mbappe")."""
    words, k = display.split(), len(q.split())
    candidates = [display] + [" ".join(words[i:i + k]) for i in range(len(words) - k + 1)]
    return max(SequenceMatcher(None, q, c).ratio() for c in candidates)


def resolve_player(name: str, players: pd.DataFrame) -> int:
    """Map a user-written name to one player_id: exact name, then all tokens, then surname.

    Token steps only look at display names ("Lionel Messi"); full legal names ("Lionel Andrés Messi
    Cuccittini") must match exactly, or a stray token like "Pele" would silently pick the wrong player.
    Anything else raises NameNotResolved with fuzzy "Did you mean" suggestions; it never substitutes.
    """
    q = _norm(name)
    display = players["player"].map(_norm)
    full = players["player_name"].map(_norm)
    tokens = [set(a.split()) for a in display]

    for match in (
        (display == q) | (full == q),
        pd.Series([set(q.split()) <= t for t in tokens], index=players.index),
        pd.Series([q.split()[-1] in t for t in tokens], index=players.index) if q else None,
    ):
        if match is None:
            continue
        hits = players[match]
        if len(hits) == 1:
            return int(hits["player_id"].iloc[0])
        if len(hits) > 1:
            raise NameNotResolved(name, [(r.player, r.team) for r in hits.head(6).itertuples()], ambiguous=True)

    scores = pd.Series([_similar(q, d) for d in display], index=players.index)
    best = scores[scores >= SUGGEST_CUTOFF].sort_values(ascending=False).head(MAX_SUGGESTIONS)
    raise NameNotResolved(name, [(players.at[i, "player"], players.at[i, "team"]) for i in best.index], ambiguous=False)


# ---------------------------------------------------------------- execution

def _round(value: float, decimals: int):
    return int(round(value)) if decimals == 0 else round(float(value), decimals)


def execute(spec: QuerySpec) -> dict:
    pm, players = load_tables()
    f = spec.filters
    meta = METRICS[spec.metric]
    per90 = spec.per90 and meta["kind"] == "count"

    rows = pm
    if f.stages:
        rows = rows[rows["stage"].isin(f.stages)]
    if f.opponents:
        rows = rows[rows["opponent"].isin(f.opponents)]
    if f.teams:
        rows = rows[rows["team"].isin(f.teams)]
    if f.position_groups:
        rows = rows[rows["position_group"].isin(f.position_groups)]
    resolved_names = None
    if f.players:
        ids = [resolve_player(n, players) for n in f.players]
        resolved_names = players.set_index("player_id").loc[ids, "player"].tolist()
        rows = rows[rows["player_id"].isin(ids)]

    sums = {"count": [spec.metric], "rate": list(meta.get("parts", ())), "minutes": []}[meta["kind"]]
    if spec.group_by == "player":
        agg = (rows.groupby("player_id")
                   .agg(player=("player", "first"), team=("team", "first"), position_group=("position_group", "first"),
                        matches=("match_id", "nunique"), minutes=("minutes", "sum"), **{c: (c, "sum") for c in sums})
                   .reset_index(drop=True))
        if f.min_minutes is not None:
            min_minutes = f.min_minutes
        elif f.players or not (per90 or meta["kind"] == "rate" or spec.sort == "asc"):
            min_minutes = 0
        else:
            min_minutes = DEFAULT_MIN_MINUTES_SUBSET if (f.stages or f.opponents) else DEFAULT_MIN_MINUTES
        agg = agg[agg["minutes"] >= min_minutes]
    else:
        # A team's minutes are the length of its matches (90 or 120), the longest player-match in each.
        match_len = rows.groupby(["match_id", "team"])["minutes"].max().groupby("team").sum()
        agg = (rows.groupby("team")
                   .agg(matches=("match_id", "nunique"), **{c: (c, "sum") for c in sums})
                   .reset_index())
        agg["minutes"] = agg["team"].map(match_len)
        min_minutes = 0

    if meta["kind"] == "rate":
        num, den = meta["parts"]
        agg["value"] = 100 * agg[num] / agg[den].replace(0, np.nan)
    elif meta["kind"] == "minutes":
        agg["value"] = agg["minutes"]
    elif per90:
        agg["value"] = agg[spec.metric] / agg["minutes"].replace(0, np.nan) * 90
    else:
        agg["value"] = agg[spec.metric]
    agg = agg.dropna(subset=["value"])
    if spec.sort == "desc" and meta["kind"] == "count" and not f.players:
        agg = agg[agg["value"] > 0]  # "top scorers in the final" should not pad with 0-goal players

    decimals = max(meta["decimals"], 2) if per90 else meta["decimals"]
    agg["value"] = [_round(v, decimals) for v in agg["value"]]
    name_col = "player" if spec.group_by == "player" else "team"
    agg = agg.sort_values(["value", name_col], ascending=[spec.sort == "asc", True])
    agg["rank"] = agg["value"].rank(method="min", ascending=spec.sort == "asc").astype(int)
    n_matching = len(agg)
    agg = agg.head(spec.limit)

    cols = ["rank", "player", "team", "position_group", "matches", "minutes", "value"] if spec.group_by == "player" \
        else ["rank", "team", "matches", "minutes", "value"]
    out = agg[cols].copy()
    out["minutes"] = out["minutes"].round().astype(int)
    return {
        "spec": spec.canonical(),
        "metric_label": meta["label"] + (" per 90" if per90 else ""),
        "interpretation": describe(spec, min_minutes, resolved_names),
        "min_minutes_applied": min_minutes,
        "n_matching": n_matching,
        "rows": out.to_dict(orient="records"),
    }
