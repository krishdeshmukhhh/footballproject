"""Sanity-check the Phase 1 metrics tables against known facts and internal invariants.

Usage: python data/sanity_check.py      (exit code 1 if any hard check fails)
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from metrics import (COUNT_METRICS, DATA_DIR, SCA_ACTION_TYPES, add_coordinates, flag_events, load_raw,
                     shot_creating_actions)

pd.set_option("display.width", 200)
failures = []


def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))
    if not ok:
        failures.append(name)


def player(players, display_name):
    row = players[players["player"] == display_name]
    assert len(row) == 1, f"{display_name!r} matched {len(row)} rows"
    return row.iloc[0]


def main():
    players = pd.read_parquet(DATA_DIR / "players.parquet")
    pm = pd.read_parquet(DATA_DIR / "player_match.parquet")
    grid = np.load(DATA_DIR / "xt_grid.npy")
    events, _, matches = load_raw()
    ev = events[events["period"] <= 4]

    print("\n== 1. Known facts (World Cup 2022) ==")
    official = matches["home_score"].sum() + matches["away_score"].sum()
    from_events = (ev["shot_outcome"] == "Goal").sum() + (ev["type"] == "Own Goal For").sum()
    check("Tournament goals = 172 (record)", official == 172 and from_events == 172,
          f"match scores {official}, rebuilt from events {from_events}")

    goal_ev = ev[(ev["shot_outcome"] == "Goal") | (ev["type"] == "Own Goal For")]
    rebuilt = goal_ev.groupby(["match_id", "team"]).size()
    agree = sum(
        rebuilt.get((r.match_id, r.home_team), 0) == r.home_score
        and rebuilt.get((r.match_id, r.away_team), 0) == r.away_score
        for r in matches.itertuples())
    check("Every match score rebuilt exactly from events", agree == len(matches), f"{agree}/{len(matches)} matches")

    expected_goals = {"Kylian Mbappé": 8, "Lionel Messi": 7, "Julián Álvarez": 4, "Olivier Giroud": 4,
                      "Gonçalo Ramos": 3, "Marcus Rashford": 3, "Álvaro Morata": 3, "Cody Gakpo": 3}
    for name, n in expected_goals.items():
        got = player(players, name)["goals"]
        check(f"{name} goals = {n}", got == n, f"got {got}")

    messi, mbappe = player(players, "Lionel Messi"), player(players, "Kylian Mbappé")
    check("Messi penalty goals = 4", messi["goals"] - messi["non_penalty_goals"] == 4,
          f"got {messi['goals'] - messi['non_penalty_goals']}")
    check("Mbappé penalty goals = 2 (both in the final)", mbappe["goals"] - mbappe["non_penalty_goals"] == 2,
          f"got {mbappe['goals'] - mbappe['non_penalty_goals']}")
    final = matches.loc[matches["competition_stage"] == "Final", "match_id"].iloc[0]
    mbappe_final = pm[(pm["match_id"] == final) & (pm["player"] == "Kylian Mbappé")]["goals"].sum()
    check("Mbappé hat-trick in the final", mbappe_final == 3, f"got {mbappe_final}")
    check("Messi played every minute: 5x90 + 2x120 = 690", messi["minutes"] == 690, f"got {messi['minutes']}")
    check("Messi appearances = 7", messi["matches"] == 7, f"got {messi['matches']}")
    print(f"  [INFO] Messi assists by StatsBomb's goal-assist flag: {messi['assists']} "
          "(FIFA credits 3; definitions differ, so this is not a hard check)")

    print("\n== 2. Internal consistency ==")
    team_min = pm.groupby(["match_id", "team"])["minutes"].sum().reset_index()
    has_et = ev.groupby("match_id")["period"].max().ge(3)
    team_min["expected"] = team_min["match_id"].map(has_et).map({True: 11 * 120, False: 11 * 90})
    team_min["diff"] = (team_min["minutes"] - team_min["expected"]).round(2)
    off = team_min[team_min["diff"].abs() > 0.01]
    red_teams = set(map(tuple, pm.loc[pm["sent_off"], ["match_id", "team"]].to_numpy()))
    unexplained = off[[(m, t) not in red_teams for m, t in zip(off["match_id"], off["team"])]]
    check("Team minutes per match = 11 x 90 (or 120), except after red cards",
          unexplained.empty, f"{len(team_min)} team-matches, {len(off)} short, all explained by red cards"
          if unexplained.empty else unexplained.to_string())
    if not off.empty:
        print(off.merge(pm.loc[pm["sent_off"], ["match_id", "team", "player"]], how="left").to_string(index=False))
    check("No player-match over 120 minutes", pm["minutes"].max() <= 120, f"max {pm['minutes'].max():.2f}")

    resum = pm.groupby("player_id")[COUNT_METRICS].sum()
    tot = players.set_index("player_id")[COUNT_METRICS]
    check("Player totals = sum of player-match rows", np.allclose(resum.loc[tot.index], tot, atol=1e-2))

    for a, b in [("progressive_passes", "passes_completed"), ("passes_completed", "passes_attempted"),
                 ("pressured_passes_completed", "pressured_passes_attempted"), ("non_penalty_goals", "goals"),
                 ("goals", "shots"), ("assists", "key_passes")]:
        bad = (players[a] > players[b]).sum()
        check(f"{a} <= {b} for every player", bad == 0, f"{bad} violations" if bad else "")
    # Cross-check SCA against StatsBomb's own pass -> shot link: a key pass must be credited
    # unless 2+ offensive actions (e.g. the shooter's dribbles) sit between it and its shot.
    fev = flag_events(add_coordinates(ev))
    fev["sca"] = shot_creating_actions(fev)
    is_action = fev["type"].isin(SCA_ACTION_TYPES) & ~((fev["type"] == "Pass") & fev["pass_outcome"].notna()) \
        & ~((fev["type"] == "Dribble") & (fev["dribble_outcome"] != "Complete"))
    shot_index = fev.set_index("id")["index"]
    kp = fev[fev["pass_assisted_shot_id"].notna()]
    mismatches = 0
    for k in kp.itertuples():
        between = fev[(fev["match_id"] == k.match_id) & (fev["possession"] == k.possession) & (fev["team"] == k.team)
                      & is_action & (fev["index"] > k.index) & (fev["index"] < shot_index[k.pass_assisted_shot_id])]
        mismatches += (k.sca > 0) != (len(between) < 2)
    check("SCA credits a key pass iff < 2 actions sit between it and its shot", mismatches == 0,
          f"{len(kp)} key passes checked, {mismatches} mismatches")

    n_shots = (ev["type"] == "Shot").sum()
    check("Total SCA <= 2 per shot", players["shot_creating_actions"].sum() <= 2 * n_shots,
          f"{players['shot_creating_actions'].sum()} SCA over {n_shots} shots "
          f"= {players['shot_creating_actions'].sum() / n_shots:.2f} per shot")
    for c in ["passes_attempted", "pressures"]:
        n_ev = (ev["type"] == {"passes_attempted": "Pass", "pressures": "Pressure"}[c]).sum()
        check(f"Every {c} event attributed to a player", players[c].sum() == n_ev,
              f"{players[c].sum()} vs {n_ev} events")
    check("xG total matches shot events", np.isclose(players["xg"].sum(), ev["shot_statsbomb_xg"].sum(), atol=0.05),
          f"{players['xg'].sum():.2f} vs {ev['shot_statsbomb_xg'].sum():.2f}")

    print("\n== 3. xT grid (16 x 12, attacking towards x = 120) ==")
    i, j = np.unravel_index(grid.argmax(), grid.shape)
    check("Highest-threat zone is in front of goal (last x-bin, central y)", i == 15 and 4 <= j <= 7,
          f"argmax bin x={i}, y={j}, xT={grid.max():.3f}")
    col_means = grid.mean(axis=1)
    check("Mean xT rises from own goal to final third", col_means[12:].mean() > col_means[:4].mean() * 5,
          " ".join(f"{v:.3f}" for v in col_means))

    print("\n== 4. Leaderboards to eyeball (min. 270 minutes) ==")
    reg = players[players["minutes"] >= 270]
    show = ["player", "team", "position_group", "minutes"]
    for metric in ["progressive_passes", "progressive_carries", "pressures", "pressured_passes_completed",
                   "shot_creating_actions", "xt_added"]:
        for col in [metric, f"{metric}_p90"]:
            top = reg.nlargest(5, col)[show + [col]]
            print(f"\n-- top 5 by {col}")
            print(top.to_string(index=False))

    print("\n== Summary ==")
    print(f"{len(players)} players, {len(pm)} player-match rows, {len(failures)} hard check(s) failed")
    if failures:
        print("FAILED:", *failures, sep="\n  ")
        sys.exit(1)


if __name__ == "__main__":
    main()
