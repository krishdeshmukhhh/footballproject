"""Executor behaviour on the real Phase 1 tables (run data/metrics.py first)."""
import pytest
from pydantic import ValidationError

from query.executor import ExecutionError, execute, load_tables, resolve_player
from query.schema import parse_spec


def run(**spec):
    return execute(parse_spec(spec))


@pytest.mark.parametrize("name, expected", [
    ("mbappe", "Kylian Mbappé"), ("Leo Messi", "Lionel Messi"),
    ("Lionel Andrés Messi Cuccittini", "Lionel Messi"), ("Vinicius", "Vinícius Júnior"),
])
def test_resolve_player(name, expected):
    _, players = load_tables()
    pid = resolve_player(name, players)
    assert players.set_index("player_id").loc[pid, "player"] == expected


@pytest.mark.parametrize("name", ["Hernández", "de jong", "Pele"])
def test_ambiguous_or_unknown_player_raises(name):
    with pytest.raises(ExecutionError):
        run(metric="goals", filters={"players": [name]})


def test_known_totals():
    assert run(metric="goals", limit=2)["rows"][0] == {
        "rank": 1, "player": "Kylian Mbappé", "team": "France", "position_group": "W",
        "matches": 7, "minutes": 597, "value": 8}
    final = run(metric="goals", filters={"stages": ["Final"]})["rows"]
    assert [(r["player"], r["value"]) for r in final] == [("Kylian Mbappé", 3), ("Lionel Messi", 2), ("Ángel Di María", 1)]


def test_team_minutes_count_extra_time():
    arg = run(metric="minutes", group_by="team", filters={"teams": ["Argentina"]})["rows"][0]
    assert arg["matches"] == 7 and arg["value"] == 5 * 90 + 2 * 120


def test_rate_metric_ignores_per90_and_applies_default_threshold():
    r = run(metric="pass_completion_pct", per90=True)
    assert r["spec"]["per90"] is False and r["min_minutes_applied"] == 270
    assert all(row["minutes"] >= 270 for row in r["rows"])


def test_named_players_skip_threshold():
    r = run(metric="pressures", per90=True, filters={"players": ["Jakić"]})
    assert r["min_minutes_applied"] == 0


def test_ties_share_rank():
    ranks = [row["rank"] for row in run(metric="goals", limit=10)["rows"]]
    assert ranks[2] == ranks[3]  # Álvarez and Giroud both on 4


def test_schema_rejects_unknown_metric_and_team():
    with pytest.raises(ValidationError):
        parse_spec('{"metric": "dribbles"}')
    with pytest.raises(ValidationError):
        parse_spec('{"metric": "goals", "filters": {"teams": ["Italy"]}}')


def test_interpretation_echo():
    r = run(metric="pressured_passes_completed", filters={"teams": ["Croatia"], "position_groups": ["CM"]})
    assert r["interpretation"] == ("The 5 players with the most passes completed under pressure, "
                                   "among central midfielders (CM), playing for Croatia, World Cup 2022.")
    r = run(metric="xt_added", per90=True, filters={"players": ["mbappe"], "stages": ["Round of 16", "Quarter-finals",
                                                                                   "Semi-finals", "3rd Place Final", "Final"]})
    assert r["interpretation"] == ("Expected threat (xT) added per 90 for Kylian Mbappé, in the knockout rounds, "
                                   "World Cup 2022.")
    r = run(metric="pass_completion_pct", sort="asc", limit=1)
    assert r["interpretation"] == ("The player with the lowest pass completion %, "
                                   "with at least 270 minutes (default threshold), World Cup 2022.")


@pytest.mark.parametrize("typo, suggestion", [
    ("Theo Hernédez", "Theo Hernández"), ("Mbape", "Kylian Mbappé"), ("De Bruyn", "Kevin De Bruyne"),
    ("Lewandowsky", "Robert Lewandowski"), ("Firas Albirkan", "Firas Albirakan"),
])
def test_typo_gets_did_you_mean_never_a_substitution(typo, suggestion):
    from query.executor import NameNotResolved
    _, players = load_tables()
    with pytest.raises(NameNotResolved) as e:
        resolve_player(typo, players)
    assert not e.value.ambiguous and e.value.suggestions[0][0] == suggestion
    assert f"Did you mean {suggestion}" in str(e.value)


def test_ambiguous_name_lists_all_candidates():
    from query.executor import NameNotResolved
    _, players = load_tables()
    with pytest.raises(NameNotResolved) as e:
        resolve_player("Hernández", players)
    assert e.value.ambiguous and {p for p, _ in e.value.suggestions} == {"Lucas Hernandez", "Theo Hernández"}


def test_possessive_names_resolve():
    _, players = load_tables()
    assert players.set_index("player_id").loc[resolve_player("Ziyech's", players), "player"] == "Hakim Ziyech"
