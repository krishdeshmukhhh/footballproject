"""Pull FIFA World Cup 2022 event data + lineups from StatsBomb open data.

Writes (all under data/raw/):
  matches.parquet   one row per match
  events.parquet    every event of every match (statsbombpy flattened format)
  spells.parquet    one row per player position spell, from the lineups

Usage: python data/pull_statsbomb.py
"""
import json
import warnings
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd
from statsbombpy import sb

COMPETITION_ID = 43  # FIFA World Cup
SEASON_ID = 106  # 2022
RAW_DIR = Path(__file__).parent / "raw"

# statsbombpy warns on every call that no credentials were given (open data needs none).
warnings.filterwarnings("ignore", message="credentials were not supplied")


def _to_parquet_safe(df: pd.DataFrame) -> pd.DataFrame:
    """Nested dict/list-of-dict columns (e.g. `tactics`) become JSON strings so pyarrow can write them."""
    df = df.copy()
    for col in df.columns:
        sample = df[col].dropna()
        if sample.empty:
            continue
        first = sample.iloc[0]
        if isinstance(first, dict) or (isinstance(first, list) and first and isinstance(first[0], dict)):
            df[col] = df[col].map(lambda v: None if v is None or (isinstance(v, float) and pd.isna(v)) else json.dumps(v))
    return df


def pull_events(match_id: int) -> pd.DataFrame:
    ev = sb.events(match_id=match_id)
    ev["match_id"] = match_id
    return ev


def pull_spells(match_id: int) -> pd.DataFrame:
    rows = []
    for team, lineup in sb.lineups(match_id=match_id).items():
        for _, p in lineup.iterrows():
            for s in p["positions"]:
                rows.append({
                    "match_id": match_id,
                    "team": team,
                    "player_id": p["player_id"],
                    "player_name": p["player_name"],
                    "player_nickname": p["player_nickname"],
                    "position": s["position"],
                    "from": s["from"],
                    "to": s["to"],
                    "from_period": s["from_period"],
                    "to_period": s["to_period"],
                    "start_reason": s["start_reason"],
                    "end_reason": s["end_reason"],
                })
    return pd.DataFrame(rows)


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    matches = sb.matches(competition_id=COMPETITION_ID, season_id=SEASON_ID)
    match_ids = sorted(matches["match_id"].tolist())
    print(f"{len(match_ids)} matches")

    with ThreadPoolExecutor(max_workers=8) as pool:
        events = list(pool.map(pull_events, match_ids))
        spells = list(pool.map(pull_spells, match_ids))

    events = pd.concat(events, ignore_index=True)
    spells = pd.concat(spells, ignore_index=True)

    _to_parquet_safe(matches).to_parquet(RAW_DIR / "matches.parquet", index=False)
    _to_parquet_safe(events).to_parquet(RAW_DIR / "events.parquet", index=False)
    spells.to_parquet(RAW_DIR / "spells.parquet", index=False)
    print(f"events: {len(events):,} rows, {events.shape[1]} cols | spells: {len(spells):,} rows")


if __name__ == "__main__":
    main()
