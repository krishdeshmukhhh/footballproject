"""Equality of specs and of execution results; shared by data generation, eval and rewards."""
import json
import math

from query.executor import ExecutionError, load_tables, resolve_player
from query.schema import QuerySpec, parse_spec


def spec_key(spec: QuerySpec | dict) -> str:
    """Canonical string for a spec, with player names resolved to ids ('Mbappe' == 'Kylian Mbappé')."""
    canon = (spec if isinstance(spec, QuerySpec) else parse_spec(spec)).canonical()
    if canon["filters"]["players"]:
        _, players = load_tables()
        ids = []
        for name in canon["filters"]["players"]:
            try:
                ids.append(str(resolve_player(name, players)))
            except ExecutionError:
                ids.append("?" + name)
        canon["filters"]["players"] = sorted(ids)
    return json.dumps(canon, sort_keys=True)


def rows_key(rows: list[dict]) -> list[tuple]:
    """Result rows as (name, value), ordered by value then name, so tie order never matters."""
    pairs = [(r.get("player", r.get("team")), r["value"]) for r in rows]
    return sorted(pairs, key=lambda p: (-p[1], p[0]))


def results_match(a: list[dict], b: list[dict], rel_tol: float = 1e-6, abs_tol: float = 1e-9) -> bool:
    ka, kb = rows_key(a), rows_key(b)
    return len(ka) == len(kb) and all(
        na == nb and math.isclose(va, vb, rel_tol=rel_tol, abs_tol=abs_tol) for (na, va), (nb, vb) in zip(ka, kb))
