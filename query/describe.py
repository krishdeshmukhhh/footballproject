"""Plain-English reading of a QuerySpec: the interpretation echo shown with every answer.

Deterministic (no LLM), and describes what the executor actually did, including default minute
thresholds and resolved player names, so a wrong reading of the question is visible to the user.
"""
from query.schema import METRICS, STAGES, QuerySpec

GROUP_NAMES = {"GK": "goalkeepers", "CB": "centre-backs", "FB": "full-backs", "DM": "defensive midfielders",
               "CM": "central midfielders", "AM": "attacking midfielders", "W": "wingers", "ST": "strikers"}
FAMILIES = {("CB", "FB"): "defenders", ("AM", "CM", "DM"): "midfielders", ("ST", "W"): "forwards"}
KNOCKOUT = sorted(s for s in STAGES if s != "Group Stage")


def _join(items: list[str]) -> str:
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def _positions(groups: list[str]) -> str:
    groups = sorted(groups)
    if tuple(groups) in FAMILIES:
        return f"{FAMILIES[tuple(groups)]} ({', '.join(groups)})"
    return _join([f"{GROUP_NAMES[g]} ({g})" for g in groups])


def _stages(stages: list[str]) -> str:
    if sorted(stages) == KNOCKOUT:
        return "the knockout rounds"
    return _join([("the " + s.lower()) if s in ("Group Stage", "Final", "3rd Place Final") else s for s in
                  sorted(stages, key=STAGES.index)])


def describe(spec: QuerySpec, min_minutes_applied: int = 0, player_names: list[str] | None = None) -> str:
    f = spec.filters
    meta = METRICS[spec.metric]
    metric = meta["label"] + (" per 90" if spec.per90 and meta["kind"] == "count" else "")

    if f.players:
        head = f"{metric} for {_join(player_names or f.players)}"
    else:
        unit = "team" if spec.group_by == "team" else "player"
        totals = meta["kind"] == "minutes" or (meta["kind"] == "count" and not spec.per90)
        order = ("most" if totals else "highest") if spec.sort == "desc" else ("fewest" if totals else "lowest")
        phrase = f"{order} {metric[0].lower() + metric[1:]}"
        head = (f"The {unit} with the {phrase}" if spec.limit == 1
                else f"The {spec.limit} {unit}s with the {phrase}")

    scope = []
    if f.position_groups:
        scope.append(("counting only " if spec.group_by == "team" else "among ") + _positions(f.position_groups))
    if f.teams:
        scope.append(("playing for " if spec.group_by == "player" else "") + _join(f.teams))
    if f.stages:
        scope.append("in " + _stages(f.stages))
    if f.opponents:
        scope.append("against " + _join(f.opponents))
    if min_minutes_applied:
        default = "" if f.min_minutes is not None else " (default threshold)"
        scope.append(f"with at least {min_minutes_applied} minutes{default}")
    return head + (", " + ", ".join(scope) if scope else "") + ", World Cup 2022."
