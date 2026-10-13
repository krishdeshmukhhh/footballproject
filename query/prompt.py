"""System prompt + few-shot examples for NL -> QuerySpec translation (shared by teacher and student).

The few-shot questions are hand-written and must never appear in the Phase 2.5 test split.
"""
import json

from query.schema import METRICS, POSITION_GROUPS, STAGES, TEAMS

METRIC_HINTS = {
    "goals": "goals scored (penalty-shootout kicks excluded)",
    "non_penalty_goals": "goals excluding penalties",
    "assists": "passes that led directly to a goal",
    "shots": "shots taken",
    "xg": "expected goals from shots",
    "npxg": "expected goals excluding penalties",
    "key_passes": "passes that led directly to a shot (aka chances created)",
    "passes_attempted": "all passes attempted",
    "passes_completed": "passes completed",
    "pass_completion_pct": "pass accuracy, % of passes completed",
    "progressive_passes": "completed passes moving the ball 10+ yards towards goal or into the box",
    "progressive_carries": "carries (dribbling with the ball) moving it 10+ yards towards goal or into the box",
    "pressures": "pressing actions on an opponent with the ball",
    "pressured_passes_attempted": "passes attempted while under pressure",
    "pressured_passes_completed": "passes completed while under pressure (press resistance)",
    "pressured_pass_completion_pct": "pass accuracy while under pressure",
    "shot_creating_actions": "the two attacking actions (passes, dribbles, fouls won, shots) leading to each shot",
    "xt_added": "expected threat added by passes and carries (how much a player moved the ball into dangerous areas)",
    "minutes": "minutes played",
}
assert set(METRIC_HINTS) == set(METRICS)

GROUP_HINTS = {"GK": "goalkeepers", "CB": "centre-backs", "FB": "full-backs and wing-backs",
               "DM": "defensive midfielders", "CM": "central midfielders", "AM": "attacking midfielders",
               "W": "wingers and wide midfielders", "ST": "strikers / centre-forwards"}

SYSTEM_PROMPT = f"""You translate football questions about the FIFA World Cup 2022 into a JSON query spec.
Output only the JSON object. Never answer the question yourself.

Fields:
- metric: one of
{chr(10).join(f'    {m}: {h}' for m, h in METRIC_HINTS.items())}
- per90: true only if the question asks for a rate ("per 90", "per game", "per match", "on average").
  Percentage metrics and minutes are never per 90.
- group_by: "player" (default) or "team" when the question ranks or asks about countries/teams as a whole.
- filters (use null for anything not mentioned):
    players: names exactly as written in the question.
    teams: the player's own team. opponents: the team they played against.
    position_groups: {", ".join(f"{g} = {h}" for g, h in GROUP_HINTS.items())}.
      Generic position words always mean the whole family: "defenders" = CB + FB,
      "midfielders"/"midfield" = DM + CM + AM, "forwards"/"attackers" = W + ST.
      Use a single group only for a specific role ("defensive midfielders" = DM, "wingers" = W).
    stages: {", ".join(STAGES)}. "knockout rounds" = every stage except Group Stage.
    min_minutes: only if the question states a playing-time threshold.
- sort: "desc" for most/top/best/highest, "asc" for fewest/least/lowest.
- limit: the number asked for ("top 3" = 3); 1 for a single "who"; 5 if unspecified and plural;
  the number of named players when the question is about specific players.

Valid team names: {", ".join(TEAMS)}. Map aliases (USA -> United States, Holland -> Netherlands, Korea -> South Korea).
Position groups: {", ".join(POSITION_GROUPS)}."""


def _spec(metric, per90=False, group_by="player", sort="desc", limit=5, **filters):
    f = {k: None for k in ["players", "teams", "position_groups", "stages", "opponents", "min_minutes"]}
    f.update(filters)
    return {"metric": metric, "per90": per90, "group_by": group_by, "filters": f, "sort": sort, "limit": limit}


KNOCKOUT = ["Round of 16", "Quarter-finals", "Semi-finals", "3rd Place Final", "Final"]

FEW_SHOT = [
    ("Who were the top 3 scorers at the tournament?", _spec("goals", limit=3)),
    ("Which full-backs made the most progressive passes per 90?",
     _spec("progressive_passes", per90=True, position_groups=["FB"])),
    ("how many progressive carries did mbappe have", _spec("progressive_carries", limit=1, players=["mbappe"])),
    ("Compare Pedri and Gavi on passes completed under pressure",
     _spec("pressured_passes_completed", limit=2, players=["Pedri", "Gavi"])),
    ("Which team pressed the most per game?", _spec("pressures", per90=True, group_by="team", limit=1)),
    ("Best pass accuracy among centre-backs with at least 300 minutes? Give me 5.",
     _spec("pass_completion_pct", position_groups=["CB"], min_minutes=300)),
    ("Who created the most shots for Argentina in the knockout rounds?",
     _spec("shot_creating_actions", limit=1, teams=["Argentina"], stages=KNOCKOUT)),
    ("Which midfielders added the least xT?", _spec("xt_added", sort="asc", position_groups=["AM", "CM", "DM"])),
    ("Who had the highest xG against Spain?", _spec("xg", limit=1, opponents=["Spain"])),
    ("Top 10 USA defenders by minutes played", _spec("minutes", limit=10, teams=["United States"],
                                                     position_groups=["CB", "FB"])),
]


def build_messages(question: str) -> list[dict]:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for q, spec in FEW_SHOT:
        messages.append({"role": "user", "content": q})
        messages.append({"role": "assistant", "content": json.dumps(spec)})
    messages.append({"role": "user", "content": question})
    return messages
