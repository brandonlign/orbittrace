"""Defensive discovery and ranking of PyTplot MMS variables."""
from __future__ import annotations

from dataclasses import dataclass
import logging
import re
from typing import Iterable

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class VariableRequest:
    spacecraft: str
    instrument: str
    quantity_tokens: tuple[str, ...]
    coordinate: str | None = None
    cadence: str = "brst"
    level: str = "l2"
    reject_tokens: tuple[str, ...] = ("error", "err", "flag", "count", "quality", "bg", "spintone")


def rank_candidates(names: Iterable[str], request: VariableRequest) -> list[tuple[float, str]]:
    """Rank candidate names; required spacecraft/instrument/quantity matches are enforced."""
    sc = request.spacecraft.lower().replace("mms", "mms")
    instrument = request.instrument.lower()
    ranked: list[tuple[float, str]] = []
    for original in names:
        name = original.lower()
        if sc not in name or instrument not in name:
            continue
        if not all(tok.lower() in name for tok in request.quantity_tokens):
            continue
        score = 10.0 + 3.0 * len(request.quantity_tokens)
        score += 3.0 if request.cadence.lower() in name else -2.0
        score += 2.0 if request.level.lower() in name else 0.0
        if request.coordinate:
            score += 5.0 if request.coordinate.lower() in name else -8.0
        score -= 20.0 * sum(tok in name for tok in request.reject_tokens)
        # FGM publishes a four-column B+|B| parent plus explicit vector/scalar
        # derivatives. Joint vector physics requires the three-component bvec.
        score += 6.0 if name.endswith("_bvec") else 0.0
        score -= 20.0 if name.endswith("_btot") else 0.0
        # Prefer exact token boundaries and data variables over metadata/support variables.
        score += sum(bool(re.search(rf"(?:^|_){re.escape(tok.lower())}(?:_|$)", name)) for tok in request.quantity_tokens)
        ranked.append((score, original))
    return sorted(ranked, key=lambda item: (-item[0], item[1]))


def resolve_variable(names: Iterable[str], request: VariableRequest, minimum_score: float = 8.0) -> str:
    """Return the best defensible variable or fail with ranked diagnostic context."""
    ranked = rank_candidates(names, request)
    if not ranked or ranked[0][0] < minimum_score:
        raise LookupError(f"No defensible variable for {request}; top candidates={ranked[:5]}")
    best_score, best = ranked[0]
    if len(ranked) > 1 and ranked[1][0] == best_score:
        raise LookupError(f"Ambiguous variable resolution for {request}: {ranked[:5]}")
    LOGGER.info("Resolved %s to %s (score %.1f); ranked=%s", request, best, best_score, ranked[:5])
    return best


PRODUCT_REQUESTS = {
    "B": lambda sc: VariableRequest(sc, "fgm", ("b",), "gse"),
    "E": lambda sc: VariableRequest(sc, "edp", ("dce",), "gse"),
    "ve": lambda sc: VariableRequest(sc, "des", ("bulkv",), "gse"),
    "ne": lambda sc: VariableRequest(sc, "des", ("numberdensity",)),
    "Pe": lambda sc: VariableRequest(sc, "des", ("prestensor",), "gse"),
    "vi": lambda sc: VariableRequest(sc, "dis", ("bulkv",), "gse"),
    "ni": lambda sc: VariableRequest(sc, "dis", ("numberdensity",)),
}
