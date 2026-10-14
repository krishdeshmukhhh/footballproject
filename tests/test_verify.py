"""Verifier behaviour on hand-written answers against a real executed result."""
import pytest

from query.executor import execute
from query.schema import parse_spec
from query.verify import correct, verify

# Mbappé 10.7, Di María 10.55, Pulisic 9.43, Vinícius Júnior 8.68, Dembélé 7.44
WINGERS = {"metric": "progressive_carries", "per90": True, "filters": {"position_groups": ["W"]}}
TAIL = "Pulisic (9.43), Vinícius (8.68) and Dembélé (7.44)."


@pytest.fixture(scope="module")
def result():
    return execute(parse_spec(WINGERS))


@pytest.mark.parametrize("answer", [
    "1. Kylian Mbappé – 10.7\n2. Ángel Di María – 10.55\n3. Christian Pulisic – 9.43\n"
    "4. Vinícius Júnior – 8.68\n5. Ousmane Dembélé – 7.44",
    "Mbappé led the wingers with 10.7 progressive carries per 90, just ahead of Di María (10.55). " + TAIL,
    "Mbappé averaged about 10.7 per 90, Di María roughly 10.6, Pulisic 9.4, Vinícius 8.7 and Dembélé 7.4.",
    "Mbappé (10.7) edged Di María (10.55) by 0.15; " + TAIL,
    "Mbappé (France) led with 10.7, then Di María (Argentina) with 10.55.",
])
def test_clean_answers_pass(result, answer):
    v = verify(answer, result, "top 5 wingers for progressive carries per 90")
    assert v.ok, v.issues


@pytest.mark.parametrize("answer, kind", [
    ("Mbappé led with 11.2, followed by Di María (10.55), " + TAIL, "number"),
    ("Mbappé led with 10.55, followed by Di María (10.7), " + TAIL, "attribution"),
    ("Mbappé led with 10.7, followed by Neymar (10.55), " + TAIL, "name"),
    ("Di María (10.55) and Mbappé (10.7) top the list, then " + TAIL, "order"),
    ("Mbappé was first with 10.7. Pulisic was second with 9.43.", "order"),
    ("France's Mbappé led with 10.7; Spain's Pulisic followed with 9.43.", "team"),
])
def test_errors_are_caught(result, answer, kind):
    v = verify(answer, result)
    assert not v.ok and kind in {i.kind for i in v.issues}, v.issues


def test_correction_fixes_attributed_numbers(result):
    answer = "Mbappé led with 10.55, followed by Di María (10.7), " + TAIL
    fixed = correct(answer, verify(answer, result), result)
    assert fixed.startswith("Mbappé led with 10.7, followed by Di María (10.55), " + TAIL)
    assert "⚠ Verification corrected 2 numbers" in fixed


def test_number_next_to_hallucinated_player_is_flagged_not_rewritten(result):
    answer = "Mbappé led with 10.7, followed by Neymar (10.55), " + TAIL
    fixed = correct(answer, verify(answer, result), result)
    assert "Neymar (10.55)" in fixed and "flagged: Neymar is not in the verified result" in fixed


def test_team_rankings():
    team = execute(parse_spec({"metric": "pressures", "per90": True, "group_by": "team", "limit": 3}))
    assert verify("Japan led with 159.69 per 90, ahead of Iran (150.67) and Morocco (147.95).", team).ok
    v = verify("Japan led with 150.67, then Iran (159.69) and Morocco (147.95).", team)
    assert {i.kind for i in v.issues} == {"attribution"}
