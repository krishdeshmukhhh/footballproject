"""Derived per-player metrics for the World Cup 2022 event data.

Reads data/raw/*.parquet (from pull_statsbomb.py) and writes:
  data/player_match.parquet   one row per (match, player) who was on the pitch
  data/players.parquet        one row per player, tournament totals + per-90
  data/xt_grid.npy            the fitted 16x12 expected-threat grid

Coordinates are StatsBomb's: 120 x 80 yards, every team attacking towards x = 120.
Penalty-shootout events (period 5) are dropped everywhere.

Metric definitions (deliberately simple; see README):
  progressive_passes     completed open-play pass starting at x >= 48 (outside own 40%) that either
                         moves the ball >= 10 yards towards goal (end_x - x >= 10) or enters the
                         penalty area from outside it
  progressive_carries    carry ending at x >= 60 (not in own half) that moves >= 10 yards towards goal,
                         or any carry entering the penalty area from outside it
  pressures              Pressure events
  pressured_passes_completed / _attempted   passes with under_pressure = True
  shot_creating_actions  for every shot, the last two offensive actions by the shooting team in the same
                         possession before it: completed passes, completed dribbles, shots, fouls won
  xt_added               sum over completed open-play passes and carries of xT(end) - xT(start)
  goals / assists / shots / xg / npxg / key_passes   straight from StatsBomb's own flags
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

DATA_DIR = Path(__file__).parent
RAW_DIR = DATA_DIR / "raw"

PITCH_X, PITCH_Y = 120.0, 80.0
BOX_X, BOX_Y_MIN, BOX_Y_MAX = 102.0, 18.0, 62.0
SET_PIECE_PASS_TYPES = {"Throw-in", "Free Kick", "Goal Kick", "Corner", "Kick Off"}
SCA_ACTION_TYPES = {"Pass", "Dribble", "Shot", "Foul Won"}
XT_BINS_X, XT_BINS_Y = 16, 12

# Nominal clock bounds of each period, in minutes. Stoppage time is clamped into the period,
# so a full match is 90 (or 120 with extra time) minutes, the usual per-90 convention.
PERIOD_BOUNDS = {1: (0, 45), 2: (45, 90), 3: (90, 105), 4: (105, 120)}

POSITION_GROUPS = {
    "Goalkeeper": "GK",
    "Right Center Back": "CB", "Center Back": "CB", "Left Center Back": "CB",
    "Right Back": "FB", "Left Back": "FB", "Right Wing Back": "FB", "Left Wing Back": "FB",
    "Right Defensive Midfield": "DM", "Center Defensive Midfield": "DM", "Left Defensive Midfield": "DM",
    "Right Center Midfield": "CM", "Center Midfield": "CM", "Left Center Midfield": "CM",
    "Right Attacking Midfield": "AM", "Center Attacking Midfield": "AM", "Left Attacking Midfield": "AM",
    "Right Midfield": "W", "Left Midfield": "W", "Right Wing": "W", "Left Wing": "W",
    "Right Center Forward": "ST", "Center Forward": "ST", "Left Center Forward": "ST", "Secondary Striker": "ST",
}

COUNT_METRICS = [
    "goals", "non_penalty_goals", "assists", "shots", "xg", "npxg", "key_passes",
    "passes_attempted", "passes_completed",
    "progressive_passes", "progressive_carries", "pressures",
    "pressured_passes_attempted", "pressured_passes_completed",
    "shot_creating_actions", "xt_added",
]


# ---------------------------------------------------------------- loading / basic helpers

def load_raw():
    events = pd.read_parquet(RAW_DIR / "events.parquet")
    spells = pd.read_parquet(RAW_DIR / "spells.parquet")
    matches = pd.read_parquet(RAW_DIR / "matches.parquet")
    return events, spells, matches


def add_coordinates(events: pd.DataFrame) -> pd.DataFrame:
    """x, y from `location`; end_x, end_y from pass/carry end locations (NaN otherwise)."""
    ev = events.copy()

    def split(col):
        arr = ev[col].map(lambda v: (v[0], v[1]) if v is not None and len(v) >= 2 else (np.nan, np.nan))
        return np.array(arr.tolist(), dtype=float).reshape(-1, 2)

    ev[["x", "y"]] = split("location")
    end = split("pass_end_location")
    carry_end = split("carry_end_location")
    is_carry = (ev["type"] == "Carry").to_numpy()
    end[is_carry] = carry_end[is_carry]
    ev[["end_x", "end_y"]] = end
    for c in ["x", "end_x"]:
        ev[c] = ev[c].clip(0, PITCH_X)
    for c in ["y", "end_y"]:
        ev[c] = ev[c].clip(0, PITCH_Y)
    return ev


def in_box(x, y):
    return (x >= BOX_X) & (y >= BOX_Y_MIN) & (y <= BOX_Y_MAX)


def nominal_minute(minute: float, period: int) -> float:
    lo, hi = PERIOD_BOUNDS[period]
    return min(max(minute, lo), hi)


# ---------------------------------------------------------------- minutes played

def player_match_minutes(events: pd.DataFrame, spells: pd.DataFrame) -> pd.DataFrame:
    """Nominal minutes per (match, player), from the event stream.

    On the pitch from kick-off (Starting XI event) or the Substitution event bringing the player
    on, until the Substitution event taking them off, a red card / second yellow, or full time.
    Temporary exits for treatment are counted as played, the usual convention.

    The lineup position spells are NOT used for timing: in several matches they run backwards
    in time or give subbed-off players a phantom spell to the final whistle.
    """
    ev = events[events["period"] <= 4].sort_values(["match_id", "period", "index"])
    full_time = ev.groupby("match_id")["period"].max().map(lambda p: PERIOD_BOUNDS[p][1])

    def at(r):
        return nominal_minute(r.minute + r.second / 60, r.period)

    on_pitch = {}  # (match_id, player_id) -> row
    for r in ev[ev["type"] == "Starting XI"].itertuples():
        for p in json.loads(r.tactics)["lineup"]:
            on_pitch[(r.match_id, p["player"]["id"])] = {
                "team": r.team, "player_name": p["player"]["name"], "start": 0.0, "end": full_time[r.match_id]}
    for r in ev[ev["type"] == "Substitution"].itertuples():
        on_pitch[(r.match_id, int(r.player_id))]["end"] = at(r)
        on_pitch[(r.match_id, int(r.substitution_replacement_id))] = {
            "team": r.team, "player_name": r.substitution_replacement, "start": at(r), "end": full_time[r.match_id]}

    red = ev[ev["foul_committed_card"].isin(["Red Card", "Second Yellow"])
             | ev["bad_behaviour_card"].isin(["Red Card", "Second Yellow"])]
    sent_off = set()
    for r in red.itertuples():
        key = (r.match_id, int(r.player_id))
        if key in on_pitch:  # a card shown on the bench has no minutes to cut
            on_pitch[key]["end"] = min(on_pitch[key]["end"], at(r))
            sent_off.add(key)

    pm = pd.DataFrame([{"match_id": m, "player_id": p, **v} for (m, p), v in on_pitch.items()])
    pm["sent_off"] = [k in sent_off for k in zip(pm["match_id"], pm["player_id"])]

    # Position for the match: the one on most of the player's events, falling back to the
    # lineup's first listed position for players with no events (e.g. stoppage-time subs).
    by_events = (ev[ev["player_id"].notna()]
                   .assign(player_id=lambda d: d["player_id"].astype(int))
                   .groupby(["match_id", "player_id"])["position"]
                   .agg(lambda s: s.mode().iloc[0] if s.notna().any() else None))
    first_listed = spells.drop_duplicates(["match_id", "player_id"]).set_index(["match_id", "player_id"])["position"]
    keys = pd.MultiIndex.from_frame(pm[["match_id", "player_id"]])
    pm["position"] = by_events.reindex(keys).fillna(first_listed.reindex(keys)).to_numpy()
    pm["player_nickname"] = pm["player_id"].map(spells.drop_duplicates("player_id").set_index("player_id")["player_nickname"])

    pm["minutes"] = (pm["end"] - pm["start"]).clip(lower=0)
    return pm.drop(columns=["start", "end"])


# ---------------------------------------------------------------- event flags

def flag_events(ev: pd.DataFrame) -> pd.DataFrame:
    """Boolean per-event columns, one per counting metric (xT and SCA are added separately)."""
    ev = ev.copy()
    is_pass = ev["type"] == "Pass"
    is_shot = ev["type"] == "Shot"
    is_penalty = ev["shot_type"] == "Penalty"
    completed_pass = is_pass & ev["pass_outcome"].isna()
    open_play_pass = is_pass & ~ev["pass_type"].isin(SET_PIECE_PASS_TYPES)
    under_pressure = ev["under_pressure"].fillna(False).astype(bool)
    enters_box = ~in_box(ev["x"], ev["y"]) & in_box(ev["end_x"], ev["end_y"])
    forward = ev["end_x"] - ev["x"]

    ev["goals"] = is_shot & (ev["shot_outcome"] == "Goal")
    ev["non_penalty_goals"] = ev["goals"] & ~is_penalty
    ev["assists"] = is_pass & ev["pass_goal_assist"].fillna(False).astype(bool)
    ev["shots"] = is_shot
    ev["xg"] = ev["shot_statsbomb_xg"].where(is_shot, 0.0).fillna(0.0)
    ev["npxg"] = ev["xg"].where(~is_penalty, 0.0)
    ev["key_passes"] = is_pass & (ev["pass_shot_assist"].fillna(False).astype(bool) | ev["assists"])
    ev["passes_attempted"] = is_pass
    ev["passes_completed"] = completed_pass
    ev["progressive_passes"] = (completed_pass & open_play_pass & (ev["x"] >= 0.4 * PITCH_X)
                                & ((forward >= 10) | enters_box))
    ev["progressive_carries"] = ((ev["type"] == "Carry")
                                 & (((forward >= 10) & (ev["end_x"] >= 0.5 * PITCH_X)) | enters_box))
    ev["pressures"] = ev["type"] == "Pressure"
    ev["pressured_passes_attempted"] = is_pass & under_pressure
    ev["pressured_passes_completed"] = completed_pass & under_pressure
    return ev


def shot_creating_actions(ev: pd.DataFrame) -> pd.Series:
    """Per-event count of shots this event was one of the two last offensive actions before.

    Offensive actions: completed passes, completed dribbles, shots and fouls won, by the shooting
    team, in the same possession, before the shot (by event index).
    """
    is_action = ev["type"].isin(SCA_ACTION_TYPES)
    is_action &= ~((ev["type"] == "Pass") & ev["pass_outcome"].notna())
    is_action &= ~((ev["type"] == "Dribble") & (ev["dribble_outcome"] != "Complete"))
    actions = ev.loc[is_action, ["match_id", "possession", "team", "index"]]

    shots = ev.loc[ev["type"] == "Shot", ["match_id", "possession", "team", "index"]]
    sca = pd.Series(0, index=ev.index)
    by_possession = {k: g.sort_values("index") for k, g in actions.groupby(["match_id", "possession", "team"])}
    for s in shots.itertuples():
        g = by_possession.get((s.match_id, s.possession, s.team))
        if g is None:
            continue
        before = g[g["index"] < s.index]
        sca.loc[before.index[-2:]] += 1
    return sca


# ---------------------------------------------------------------- expected threat

def _zone(x, y):
    zx = np.clip((np.asarray(x) / PITCH_X * XT_BINS_X).astype(int), 0, XT_BINS_X - 1)
    zy = np.clip((np.asarray(y) / PITCH_Y * XT_BINS_Y).astype(int), 0, XT_BINS_Y - 1)
    return zx * XT_BINS_Y + zy


def fit_xt(ev: pd.DataFrame, n_iter: int = 50) -> np.ndarray:
    """Zone-based expected threat (Karun Singh, 2018) fitted on this tournament.

    Moves are open-play passes and carries (completed or not); shots exclude penalties. To cut
    noise from 64 matches, a zone's scoring probability is the mean StatsBomb xG of its shots
    rather than its raw goal rate. Returns a (16, 12) grid indexed [x_bin, y_bin].
    """
    n = XT_BINS_X * XT_BINS_Y
    is_move = ((ev["type"] == "Pass") & ~ev["pass_type"].isin(SET_PIECE_PASS_TYPES)) | (ev["type"] == "Carry")
    is_shot = (ev["type"] == "Shot") & (ev["shot_type"] != "Penalty")
    moves, shots = ev[is_move], ev[is_shot]
    move_ok = moves[(moves["type"] == "Carry") | moves["pass_outcome"].isna()]

    move_count = np.bincount(_zone(moves["x"], moves["y"]), minlength=n).astype(float)
    shot_count = np.bincount(_zone(shots["x"], shots["y"]), minlength=n).astype(float)
    xg_sum = np.bincount(_zone(shots["x"], shots["y"]), weights=shots["shot_statsbomb_xg"], minlength=n)

    total = move_count + shot_count
    with np.errstate(divide="ignore", invalid="ignore"):
        p_shot = np.where(total > 0, shot_count / total, 0.0)
        p_move = np.where(total > 0, move_count / total, 0.0)
        p_goal = np.where(shot_count > 0, xg_sum / shot_count, 0.0)

    transitions = np.zeros((n, n))
    np.add.at(transitions, (_zone(move_ok["x"], move_ok["y"]), _zone(move_ok["end_x"], move_ok["end_y"])), 1)
    with np.errstate(divide="ignore", invalid="ignore"):
        transitions = np.where(move_count[:, None] > 0, transitions / move_count[:, None], 0.0)

    xt = np.zeros(n)
    for _ in range(n_iter):
        xt = p_shot * p_goal + p_move * (transitions @ xt)
    return xt.reshape(XT_BINS_X, XT_BINS_Y)


def xt_added(ev: pd.DataFrame, grid: np.ndarray) -> pd.Series:
    flat = grid.reshape(-1)
    credited = (((ev["type"] == "Pass") & ev["pass_outcome"].isna() & ~ev["pass_type"].isin(SET_PIECE_PASS_TYPES))
                | (ev["type"] == "Carry"))
    out = pd.Series(0.0, index=ev.index)
    sub = ev[credited]
    out.loc[sub.index] = flat[_zone(sub["end_x"], sub["end_y"])] - flat[_zone(sub["x"], sub["y"])]
    return out


# ---------------------------------------------------------------- tables

def build_tables():
    events, spells, matches = load_raw()
    ev = add_coordinates(events[events["period"] <= 4])
    ev = flag_events(ev)
    ev["shot_creating_actions"] = shot_creating_actions(ev)
    grid = fit_xt(ev)
    ev["xt_added"] = xt_added(ev, grid)

    minutes = player_match_minutes(events, spells)

    on_ball = ev[ev["player_id"].notna()].copy()
    on_ball["player_id"] = on_ball["player_id"].astype(int)
    counts = on_ball.groupby(["match_id", "player_id"])[COUNT_METRICS].sum().reset_index()

    pm = minutes.merge(counts, on=["match_id", "player_id"], how="left")
    pm[COUNT_METRICS] = pm[COUNT_METRICS].fillna(0)
    int_cols = [c for c in COUNT_METRICS if c not in ("xg", "npxg", "xt_added")]
    pm[int_cols] = pm[int_cols].astype(int)

    # Events by players with no lineup minutes (an unused sub booked on the bench) carry no
    # metric counts; guard against that silently changing.
    orphan = counts.merge(minutes[["match_id", "player_id"]], how="left", indicator=True)
    orphan = orphan[orphan["_merge"] == "left_only"]
    assert orphan[COUNT_METRICS].to_numpy().sum() == 0, f"metric events with no lineup row:\n{orphan}"

    m = matches.set_index("match_id")
    pm["stage"] = pm["match_id"].map(m["competition_stage"])
    pm["match_date"] = pm["match_id"].map(m["match_date"])
    home = pm["match_id"].map(m["home_team"])
    away = pm["match_id"].map(m["away_team"])
    pm["opponent"] = np.where(pm["team"] == home, away, home)
    pm["position_group"] = pm["position"].map(POSITION_GROUPS)
    pm["player"] = pm["player_nickname"].fillna(pm["player_name"])

    players = aggregate_players(pm)
    return pm, players, grid


def aggregate_players(pm: pd.DataFrame) -> pd.DataFrame:
    pos_minutes = pm.groupby(["player_id", "position"])["minutes"].sum().reset_index()
    primary = (pos_minutes.sort_values("minutes", ascending=False)
                          .drop_duplicates("player_id").set_index("player_id")["position"])

    players = (pm.groupby("player_id")
                 .agg(player=("player", "first"), player_name=("player_name", "first"), team=("team", "first"),
                      matches=("match_id", "nunique"), minutes=("minutes", "sum"),
                      **{c: (c, "sum") for c in COUNT_METRICS})
                 .reset_index())
    players["primary_position"] = players["player_id"].map(primary)
    players["position_group"] = players["primary_position"].map(POSITION_GROUPS)
    players["minutes"] = players["minutes"].round(1)
    # Stoppage-time cameos have 0 nominal minutes; their per-90 values are undefined (NaN).
    per90_minutes = players["minutes"].replace(0, np.nan)
    for c in COUNT_METRICS:
        players[f"{c}_p90"] = (players[c] / per90_minutes * 90).round(3)
    players["pressured_pass_completion_pct"] = (
        100 * players["pressured_passes_completed"] / players["pressured_passes_attempted"].replace(0, np.nan)
    ).round(1)
    for c in ["xg", "npxg", "xt_added"]:
        players[c] = players[c].round(3)

    lead = ["player_id", "player", "player_name", "team", "primary_position", "position_group", "matches", "minutes"]
    return players[lead + [c for c in players.columns if c not in lead]]


def main():
    pm, players, grid = build_tables()
    pm.to_parquet(DATA_DIR / "player_match.parquet", index=False)
    players.to_parquet(DATA_DIR / "players.parquet", index=False)
    np.save(DATA_DIR / "xt_grid.npy", grid)
    print(f"player_match: {len(pm):,} rows | players: {len(players):,} rows")


if __name__ == "__main__":
    main()
