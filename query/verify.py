"""Verify an LLM-written answer against the executed result, and correct what can be corrected.

Three checks, all against the ground-truth rows the executor returned:
  numbers   every number must match a value in the result (to the precision written). Each number is
            tied to the nearest player/team mention in its sentence; a number that belongs to another
            row ("Messi 71" when 71 is Mbappé's) is an attribution error.
  names     every player or team mentioned must be in the result (or named in the question's filters).
  order     for rankings, entities must first appear in rank order, and ordinals ("Messi was
            second") must match their rank. Tied ranks may appear in either order.

`correct()` rewrites numbers that are tied to a known entity, and appends a flagged correction with the
verified rows for everything else. No LLM involved.
"""
import re
import unicodedata
from dataclasses import asdict, dataclass, field
from functools import lru_cache
from itertools import combinations

from query.executor import DEFAULT_MIN_MINUTES, DEFAULT_MIN_MINUTES_SUBSET, load_tables
from query.schema import TEAMS

WORD_NUMBERS = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen "
    "seventeen eighteen nineteen twenty".split())}
ORDINALS = {w: i + 1 for i, w in enumerate("first second third fourth fifth sixth seventh eighth ninth tenth".split())}
TEAM_ALIASES = {  # alias -> team; aliases in CAPS must match case-sensitively
    "Argentine": "Argentina", "Argentinian": "Argentina", "Australian": "Australia", "Belgian": "Belgium",
    "Brazilian": "Brazil", "Cameroonian": "Cameroon", "Canadian": "Canada", "Costa Rican": "Costa Rica",
    "Croatian": "Croatia", "Danish": "Denmark", "Ecuadorian": "Ecuador", "English": "England", "French": "France",
    "German": "Germany", "Ghanaian": "Ghana", "Iranian": "Iran", "Japanese": "Japan", "Mexican": "Mexico",
    "Moroccan": "Morocco", "Dutch": "Netherlands", "Holland": "Netherlands", "Polish": "Poland",
    "Portuguese": "Portugal", "Qatari": "Qatar", "Saudi": "Saudi Arabia", "Senegalese": "Senegal",
    "Serbian": "Serbia", "Korea": "South Korea", "Korean": "South Korea", "South Korean": "South Korea",
    "Spanish": "Spain", "Swiss": "Switzerland", "Tunisian": "Tunisia", "USA": "United States",
    "US": "United States", "USMNT": "United States", "American": "United States", "Uruguayan": "Uruguay",
    "Welsh": "Wales",
}
NUMBER_RE = re.compile(r"(?<![\w.])(\d+(?:,\d{3})*(?:\.\d+)?)(?:\s?(%|percent))?(?!\w)")
ORDINAL_RE = re.compile(r"\b(\d+)(?:st|nd|rd|th)\b|\b(" + "|".join(ORDINALS) + r")\b", re.I)
WORD_NUMBER_RE = re.compile(r"\b(" + "|".join(WORD_NUMBERS) + r")\b", re.I)
LIST_MARKER_RE = re.compile(r"^\s*(\d+)[.)]\s", re.M)


@dataclass
class Issue:
    kind: str           # number | attribution | name | team | order
    claim: str          # the offending text
    detail: str
    span: tuple[int, int] | None = None
    expected: str | None = None   # replacement text, when the fix is unambiguous


@dataclass
class Verification:
    ok: bool
    issues: list[Issue] = field(default_factory=list)
    numbers_checked: int = 0
    entities_found: list[str] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)

    @property
    def hallucinated_number(self) -> bool:
        return any(i.kind in ("number", "attribution") for i in self.issues)


# ---------------------------------------------------------------- text helpers

def _fold(text: str) -> tuple[str, list[int]]:
    """Accent-stripped lowercase text, plus a map from folded index to original index."""
    out, index = [], []
    for i, ch in enumerate(text):
        for c in unicodedata.normalize("NFKD", ch).encode("ascii", "ignore").decode().lower():
            out.append(c)
            index.append(i)
    return "".join(out), index


def _sentence_ids(text: str) -> list[int]:
    """Sentence number of every character: splits on . ! ? ; and newlines (not decimal points)."""
    ids, sid = [], 0
    for i, ch in enumerate(text):
        ids.append(sid)
        decimal = ch == "." and 0 < i < len(text) - 1 and text[i - 1].isdigit() and text[i + 1].isdigit()
        if (ch in ".!?;\n" and not decimal):
            sid += 1
    return ids


def _fmt(value) -> str:
    return f"{value:,}" if isinstance(value, int) else str(value)


def _decimals(x: float) -> int:
    text = repr(float(x))
    return 0 if text.endswith(".0") else len(text.split(".")[1])


def _matches(claim: float, decimals: int, truth: float) -> bool:
    """True if `claim`, written with `decimals` decimals, is `truth` rounded to that precision. A claim more
    precise than the stored truth (10.554 vs a stored 10.55) is compared at the truth's precision."""
    if decimals > _decimals(truth):
        return abs(round(claim, _decimals(truth)) - truth) <= 1e-9
    return abs(claim - truth) <= 0.5 * 10 ** -decimals + 1e-9


# ---------------------------------------------------------------- entity index

@lru_cache(maxsize=1)
def entity_variants() -> list[tuple[str, str, str, bool]]:
    """(folded variant, entity key, display label, needs capital) for every player and team.

    Players are found by full display name, by any single name token unique to one player
    ("Mbappé", "Vinícius", "Kylian"), and mononyms ("Rodri") by themselves. Short or shared tokens
    are skipped to avoid false hits.
    """
    _, players = load_tables()
    out = []
    tokens = {}
    for r in players.itertuples():
        folded = _fold(r.player)[0]
        out.append((folded, f"player:{r.player}", r.player, True))
        words = folded.split()
        if len(words) > 1:
            for w in set(words):
                tokens.setdefault(w, set()).add(r.player)
    team_words = {w for t in TEAMS for w in _fold(t)[0].split()} | {"world", "cup"}
    for token, owners in tokens.items():
        if len(owners) == 1 and len(token) >= 4 and token not in team_words:
            owner = next(iter(owners))
            out.append((token, f"player:{owner}", owner, True))
    for t in TEAMS:
        out.append((_fold(t)[0], f"team:{t}", t, True))
    for alias, t in TEAM_ALIASES.items():
        out.append((_fold(alias)[0] if not alias.isupper() else alias, f"team:{t}", t, True))
    return sorted(out, key=lambda v: -len(v[0]))


def find_entities(text: str) -> list[tuple[int, int, str]]:
    """Non-overlapping (start, end, entity key) mentions in original-text coordinates, longest first."""
    folded, index = _fold(text)
    taken, found = set(), []
    for variant, key, _, needs_cap in entity_variants():
        haystack = text if variant.isupper() else folded
        for m in re.finditer(r"(?<![\w-])" + re.escape(variant) + r"(?![\w-])", haystack):
            a, b = (m.start(), m.end()) if variant.isupper() else (index[m.start()], index[m.end() - 1] + 1)
            if needs_cap and not text[a].isupper():
                continue
            if any(i in taken for i in range(a, b)):
                continue
            taken.update(range(a, b))
            found.append((a, b, key))
    return sorted(found)


# ---------------------------------------------------------------- verification

def _row_key(row) -> str:
    return f"player:{row['player']}" if "player" in row else f"team:{row['team']}"


def _unrecognised_name_between(text, mentions, owner, number) -> bool:
    """True if a capitalised word that is not part of any recognised mention lies between the owner
    mention and the number (sentence-initial words excluded)."""
    lo, hi = (owner[1], number[0]) if owner[1] <= number[0] else (number[1], owner[0])
    covered = {i for a, b, _ in mentions for i in range(a, b)}
    for m in re.finditer(r"\b[A-ZÀ-Ý][\wÀ-ÿ'-]+", text[lo:hi]):
        start = lo + m.start()
        if start in covered:
            continue
        prev = text[:start].rstrip()
        if not prev or prev[-1] in ".!?:\n(":
            continue
        return True
    return False


def verify(answer: str, result: dict, question: str = "", extra_truth: dict | None = None) -> Verification:
    """Check `answer` against `result` (an executor output). `extra_truth` maps entity key -> extra true
    numbers for that entity (used when scoring free-form baselines that may cite other true stats)."""
    rows = result["rows"]
    spec = result["spec"]
    by_key = {_row_key(r): r for r in rows}
    issues: list[Issue] = []

    # Allowed numbers per entity, and numbers allowed anywhere.
    own = {k: [r["value"], r["minutes"], r["matches"]] for k, r in by_key.items()}
    for k, extra in (extra_truth or {}).items():
        own.setdefault(k, []).extend(extra)
    values = [r["value"] for r in rows]
    generic = [90, 2022, spec["limit"], len(rows), result["min_minutes_applied"], *range(1, len(rows) + 1),
               DEFAULT_MIN_MINUTES, DEFAULT_MIN_MINUTES_SUBSET]  # quoting a threshold convention is not a stat
    generic += [round(abs(a - b), 3) for a, b in combinations(values, 2)]
    generic += [round(a + b, 3) for a, b in combinations(values, 2)]
    generic += [float(n.replace(",", "")) for n, _ in NUMBER_RE.findall(question)]
    generic += [WORD_NUMBERS[w.lower()] for w in WORD_NUMBER_RE.findall(question)]

    # Entities mentioned.
    mentions = find_entities(answer)
    allowed_entities = set(by_key)
    allowed_entities |= {f"team:{t}" for t in (spec["filters"]["teams"] or []) + (spec["filters"]["opponents"] or [])}
    allowed_entities |= {f"team:{r['team']}" for r in rows if "player" in r}
    named = {k for k in by_key if k.startswith("player:")} if spec["filters"]["players"] else set()
    for a, b, key in mentions:
        if key not in allowed_entities and key not in named:
            kind = "name" if key.startswith("player:") else "team"
            issues.append(Issue(kind, answer[a:b], f"{key.split(':', 1)[1]} is not in the verified result", (a, b)))

    # Numbers, each tied to the nearest row entity in the same sentence (preceding preferred).
    sentence = _sentence_ids(answer)
    row_mentions = [(a, b, k) for a, b, k in mentions if k in by_key]
    row_type = "team:" if spec["group_by"] == "team" else "player:"
    owner_mentions = [m for m in mentions if m[2].startswith(row_type)]
    list_markers = {m.start(1) for m in LIST_MARKER_RE.finditer(answer)}
    claims = [(m.start(1), m.end(1), float(m.group(1).replace(",", "")),
               len(m.group(1).split(".")[1]) if "." in m.group(1) else 0) for m in NUMBER_RE.finditer(answer)]
    claims += [(m.start(), m.end(), float(WORD_NUMBERS[m.group(1).lower()]), 0) for m in WORD_NUMBER_RE.finditer(answer)]
    ordinal_spans = {m.start() for m in ORDINAL_RE.finditer(answer)}
    checked = 0
    for a, b, claim, decimals in sorted(claims):
        if a in list_markers or a in ordinal_spans or (decimals == 0 and 1900 <= claim <= 2100):
            continue
        checked += 1
        # Candidates are mentions of the row type (players, or teams for team rankings), including ones
        # not in the result: a number next to a hallucinated player is not re-attributed to a real one.
        same = [m for m in owner_mentions if sentence[m[0]] == sentence[a]]
        before = [m for m in same if m[1] <= a]
        owner = (before[-1] if before else min(same, key=lambda m: m[0] - b)) if same else None
        if owner and (owner[2] not in by_key or _unrecognised_name_between(answer, mentions, owner, (a, b))):
            owner = None  # never guess who the number belongs to
        if owner and any(_matches(claim, decimals, t) for t in own[owner[2]]):
            continue
        if any(_matches(claim, decimals, t) for t in generic):
            continue
        # Attribution means the number is another result row's value (not its minutes or match count).
        others = [k for k, r in by_key.items() if owner and k != owner[2] and _matches(claim, decimals, r["value"])]
        if owner and others:
            issues.append(Issue("attribution", answer[a:b],
                                f"{answer[a:b]} belongs to {others[0].split(':', 1)[1]}, not {owner[2].split(':', 1)[1]} "
                                f"(whose value is {_fmt(by_key[owner[2]]['value'])})",
                                (a, b), _fmt(by_key[owner[2]]["value"])))
        elif owner:
            issues.append(Issue("number", answer[a:b],
                                f"{answer[a:b]} for {owner[2].split(':', 1)[1]} is not in the result "
                                f"(verified value {_fmt(by_key[owner[2]]['value'])})",
                                (a, b), _fmt(by_key[owner[2]]["value"])))
        elif not any(any(_matches(claim, decimals, t) for t in nums) for nums in own.values()):
            issues.append(Issue("number", answer[a:b], f"{answer[a:b]} does not appear in the verified result", (a, b)))

    # Ranking order and ordinal claims.
    rank = {k: r["rank"] for k, r in by_key.items()}
    if not spec["filters"]["players"] and len(rows) > 1:
        seen, last = set(), None
        for a, b, key in row_mentions:
            if key in seen:
                continue
            seen.add(key)
            if last and rank[key] < rank[last[2]]:
                issues.append(Issue("order", answer[a:b], f"{key.split(':', 1)[1]} (rank {rank[key]}) is listed after "
                                    f"{last[2].split(':', 1)[1]} (rank {rank[last[2]]})", (a, b)))
            last = (a, b, key)
        for m in ORDINAL_RE.finditer(answer):
            n = int(m.group(1)) if m.group(1) else ORDINALS[m.group(2).lower()]
            same = [x for x in row_mentions if sentence[x[0]] == sentence[m.start()]]
            if len(same) == 1 and rank[same[0][2]] != n:
                issues.append(Issue("order", m.group(0), f"{same[0][2].split(':', 1)[1]} is ranked "
                                    f"{rank[same[0][2]]}, not {m.group(0)}", (m.start(), m.end())))

    return Verification(ok=not issues, issues=issues, numbers_checked=checked,
                        entities_found=sorted({k for _, _, k in mentions}))


def verified_rows_text(result: dict) -> str:
    return "; ".join(f"{r['rank']}. {r.get('player', r.get('team'))}: {_fmt(r['value'])}" for r in result["rows"])


def correct(answer: str, verification: Verification, result: dict) -> str:
    """Fix numbers tied to a known entity in place; flag everything else with the verified rows."""
    if verification.ok:
        return answer
    fixed = answer
    fixable = sorted((i for i in verification.issues if i.expected and i.span), key=lambda i: -i.span[0])
    for issue in fixable:
        a, b = issue.span
        fixed = fixed[:a] + issue.expected + fixed[b:]
    flagged = [i for i in verification.issues if i not in fixable]
    notes = []
    if fixable:
        notes.append(f"corrected {len(fixable)} number{'s' if len(fixable) > 1 else ''} to the verified values")
    if flagged:
        notes.append("flagged: " + "; ".join(i.detail for i in flagged))
    return f"{fixed}\n\n⚠ Verification {' and '.join(notes)}. Verified result: {verified_rows_text(result)}."
