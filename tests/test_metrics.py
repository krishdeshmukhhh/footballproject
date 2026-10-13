"""Boundary tests for the Phase 1 metric definitions, on hand-built events."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "data"))
from metrics import flag_events, nominal_minute, shot_creating_actions  # noqa: E402


def make_events(rows):
    """Build an events frame with the columns flag_events needs; unspecified fields are null."""
    base = {
        "match_id": 1, "possession": 1, "team": "A", "period": 1, "type": "Pass",
        "x": 60.0, "y": 40.0, "end_x": np.nan, "end_y": np.nan,
        "pass_outcome": None, "pass_type": None, "pass_goal_assist": None, "pass_shot_assist": None,
        "shot_outcome": None, "shot_type": None, "shot_statsbomb_xg": np.nan,
        "under_pressure": None, "dribble_outcome": None,
    }
    df = pd.DataFrame([{**base, **r} for r in rows])
    df["index"] = range(len(df))
    return df


@pytest.mark.parametrize("x, end_x, end_y, extra, expected", [
    (60, 70, 40, {}, True),                                # exactly 10 yards forward
    (60, 69.9, 40, {}, False),                             # just short of 10 yards
    (47.9, 70, 40, {}, False),                             # starts in own 40% of the pitch
    (48, 58, 40, {}, True),                                # starts on the 40% line
    (95, 103, 40, {}, True),                               # < 10 yards but enters the box
    (103, 115, 40, {}, True),                              # 10+ yards inside the box
    (103, 108, 40, {}, False),                             # < 10 yards, already in the box
    (95, 103, 10, {}, False),                              # past x=102 but wide of the box
    (60, 80, 40, {"pass_outcome": "Incomplete"}, False),   # incomplete
    (60, 80, 40, {"pass_type": "Free Kick"}, False),       # set piece
    (60, 80, 40, {"pass_type": "Recovery"}, True),         # open-play pass type
])
def test_progressive_pass(x, end_x, end_y, extra, expected):
    ev = flag_events(make_events([{"x": x, "end_x": end_x, "end_y": end_y, **extra}]))
    assert bool(ev["progressive_passes"].iloc[0]) is expected


@pytest.mark.parametrize("x, end_x, expected", [
    (50, 60, True),     # 10 yards, ends on the halfway line
    (45, 55, False),    # 10 yards but ends in own half
    (70, 79, False),    # 9 yards
    (95, 103, True),    # enters the box
])
def test_progressive_carry(x, end_x, expected):
    ev = flag_events(make_events([{"type": "Carry", "x": x, "end_x": end_x, "end_y": 40}]))
    assert bool(ev["progressive_carries"].iloc[0]) is expected


def test_pressured_passes_and_penalty_split():
    ev = flag_events(make_events([
        {"under_pressure": True},
        {"under_pressure": True, "pass_outcome": "Incomplete"},
        {"type": "Shot", "shot_type": "Penalty", "shot_outcome": "Goal", "shot_statsbomb_xg": 0.78},
        {"type": "Shot", "shot_type": "Open Play", "shot_outcome": "Goal", "shot_statsbomb_xg": 0.2},
    ]))
    assert ev["pressured_passes_attempted"].sum() == 2
    assert ev["pressured_passes_completed"].sum() == 1
    assert ev["goals"].sum() == 2 and ev["non_penalty_goals"].sum() == 1
    assert ev["xg"].sum() == pytest.approx(0.98) and ev["npxg"].sum() == pytest.approx(0.2)


def test_sca_takes_last_two_actions_of_shooting_team_in_possession():
    ev = make_events([
        {"type": "Pass"},                                         # 0: third-last action, not credited
        {"type": "Pass", "pass_outcome": "Incomplete"},           # 1: incomplete, not an action
        {"type": "Pressure", "team": "B"},                        # 2: opponent, ignored
        {"type": "Dribble", "dribble_outcome": "Incomplete"},     # 3: failed dribble, not an action
        {"type": "Foul Won"},                                     # 4: second-last action
        {"type": "Pass"},                                         # 5: last action
        {"type": "Shot"},                                         # 6: the shot
        {"type": "Pass", "possession": 2},                        # 7: next possession
        {"type": "Shot", "possession": 2},                        # 8: shot with one prior action
    ])
    assert shot_creating_actions(ev).tolist() == [0, 0, 0, 0, 1, 1, 0, 1, 0]


def test_sca_rebound_shot_counts():
    ev = make_events([{"type": "Pass"}, {"type": "Shot"}, {"type": "Shot"}])
    # The first shot creates the rebound; the pass created both shots.
    assert shot_creating_actions(ev).tolist() == [2, 1, 0]


@pytest.mark.parametrize("minute, period, expected", [
    (47.5, 1, 45),     # first-half stoppage clamps to 45
    (44.0, 2, 45),     # (impossible) early second-half clock clamps up to 45
    (93.2, 2, 90),     # second-half stoppage clamps to 90
    (100.0, 3, 100),
    (121.0, 4, 120),
])
def test_nominal_minute(minute, period, expected):
    assert nominal_minute(minute, period) == expected
