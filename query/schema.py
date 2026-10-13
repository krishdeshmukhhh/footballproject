"""The constrained query spec the LLM must emit, and the metric catalog it can ask about.

`QuerySpec` is the single source of truth: its JSON schema drives vLLM guided decoding, and
`parse_spec` validates and canonicalises whatever the model returns. The LLM never writes pandas.
"""
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

# kind: "count" sums and can be per-90; "rate" is recomputed from its parts and is never per-90;
# "minutes" is playing time itself. decimals: rounding of the reported value (per-90 uses 2 if 0).
METRICS = {
    "goals": {"label": "Goals", "kind": "count", "decimals": 0},
    "non_penalty_goals": {"label": "Non-penalty goals", "kind": "count", "decimals": 0},
    "assists": {"label": "Assists", "kind": "count", "decimals": 0},
    "shots": {"label": "Shots", "kind": "count", "decimals": 0},
    "xg": {"label": "Expected goals (xG)", "kind": "count", "decimals": 2},
    "npxg": {"label": "Non-penalty xG", "kind": "count", "decimals": 2},
    "key_passes": {"label": "Key passes", "kind": "count", "decimals": 0},
    "passes_attempted": {"label": "Passes attempted", "kind": "count", "decimals": 0},
    "passes_completed": {"label": "Passes completed", "kind": "count", "decimals": 0},
    "pass_completion_pct": {"label": "Pass completion %", "kind": "rate", "decimals": 1,
                            "parts": ("passes_completed", "passes_attempted")},
    "progressive_passes": {"label": "Progressive passes (simplified)", "kind": "count", "decimals": 0},
    "progressive_carries": {"label": "Progressive carries", "kind": "count", "decimals": 0},
    "pressures": {"label": "Pressures", "kind": "count", "decimals": 0},
    "pressured_passes_attempted": {"label": "Passes attempted under pressure", "kind": "count", "decimals": 0},
    "pressured_passes_completed": {"label": "Passes completed under pressure", "kind": "count", "decimals": 0},
    "pressured_pass_completion_pct": {"label": "Pass completion % under pressure", "kind": "rate", "decimals": 1,
                                      "parts": ("pressured_passes_completed", "pressured_passes_attempted")},
    "shot_creating_actions": {"label": "Shot-creating actions", "kind": "count", "decimals": 0},
    "xt_added": {"label": "Expected threat (xT) added", "kind": "count", "decimals": 3},
    "minutes": {"label": "Minutes played", "kind": "minutes", "decimals": 0},
}

POSITION_GROUPS = ["GK", "CB", "FB", "DM", "CM", "AM", "W", "ST"]

TEAMS = [
    "Argentina", "Australia", "Belgium", "Brazil", "Cameroon", "Canada", "Costa Rica", "Croatia",
    "Denmark", "Ecuador", "England", "France", "Germany", "Ghana", "Iran", "Japan",
    "Mexico", "Morocco", "Netherlands", "Poland", "Portugal", "Qatar", "Saudi Arabia", "Senegal",
    "Serbia", "South Korea", "Spain", "Switzerland", "Tunisia", "United States", "Uruguay", "Wales",
]

STAGES = ["Group Stage", "Round of 16", "Quarter-finals", "Semi-finals", "3rd Place Final", "Final"]

Metric = Literal[tuple(METRICS)]
PositionGroup = Literal[tuple(POSITION_GROUPS)]
Team = Literal[tuple(TEAMS)]
Stage = Literal[tuple(STAGES)]


class Filters(BaseModel):
    model_config = ConfigDict(extra="forbid")

    players: list[str] | None = Field(None, description="Player names as the user wrote them; resolved later.")
    teams: list[Team] | None = None
    position_groups: list[PositionGroup] | None = None
    stages: list[Stage] | None = None
    opponents: list[Team] | None = None
    min_minutes: int | None = Field(None, ge=0, le=720)

    @field_validator("players", "teams", "position_groups", "stages", "opponents")
    @classmethod
    def _empty_is_none(cls, v):
        # [] and null mean the same thing; canonicalise to null and sort for stable comparison.
        return sorted(set(v)) if v else None


class QuerySpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    metric: Metric
    per90: bool = False
    group_by: Literal["player", "team"] = "player"
    filters: Filters = Field(default_factory=Filters)
    sort: Literal["desc", "asc"] = "desc"
    limit: int = Field(5, ge=1, le=20)

    def canonical(self) -> dict:
        """Normalised dict: per90 dropped where it is meaningless, so equal intents compare equal."""
        spec = self.model_dump()
        if METRICS[self.metric]["kind"] != "count":
            spec["per90"] = False
        return spec


def json_schema() -> dict:
    return QuerySpec.model_json_schema()


def parse_spec(text_or_dict) -> QuerySpec:
    """Validate raw LLM output (JSON text or dict). Raises pydantic.ValidationError if invalid."""
    if isinstance(text_or_dict, str):
        return QuerySpec.model_validate_json(text_or_dict)
    return QuerySpec.model_validate(text_or_dict)
