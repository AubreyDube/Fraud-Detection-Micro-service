import json
import logging
import uuid
from pathlib import Path
from typing import Dict, Any, Callable, Tuple, List

import jsonschema

logger = logging.getLogger("fraud_detector")
_handler = logging.StreamHandler()
_handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(_handler)
logger.setLevel(logging.INFO)

with open(Path(__file__).with_name("eventSchema.json")) as _f:
    _EVENT_SCHEMA = json.load(_f)

Rule = Tuple[str, Callable[[Dict[str, Any], Dict[str, Any]], bool]]
_RULES: List[Rule] = [
    ("amount_gt_1000", lambda tx, feats: tx.get("amount", 0) > 1000),
    ("velocity_score_high", lambda tx, feats: feats.get("velocity_score", 0) > 0.8),
    ("high_risk_country", lambda tx, feats: feats.get("is_high_risk_country")),
]
_TOTAL_RULES = len(_RULES)


def _log(entry: Dict[str, Any], correlation_id: str) -> None:
    log_record = {"correlation_id": correlation_id, **entry}
    logger.info(json.dumps(log_record))


def evaluate_transaction(event: Dict[str, Any], correlation_id: str | None = None) -> Dict[str, Any]:
    """Return fraud decision for a transaction event.

    Parameters
    ----------
    event: mapping conforming to the event schema
    correlation_id: optional UUID used to correlate logs across services. If
        omitted or invalid, a new UUID4 will be generated.
    """
    if correlation_id:
        try:
            uuid.UUID(correlation_id)
        except (ValueError, AttributeError, TypeError):
            correlation_id = str(uuid.uuid4())
    else:
        correlation_id = str(uuid.uuid4())
    try:
        jsonschema.validate(event, _EVENT_SCHEMA)
    except jsonschema.ValidationError as err:
        _log({"event_id": event.get("event_id"), "error": err.message}, correlation_id)
        raise

    tx = event.get("transaction", {})
    features = event.get("features", {})
    reasons = [name for name, rule in _RULES if rule(tx, features)]

    is_fraud = bool(reasons)
    score = min(1.0, len(reasons) / _TOTAL_RULES)
    decision = {"fraud": is_fraud, "score": score, "reasons": reasons}

    _log({"event_id": event.get("event_id"), "decision": decision}, correlation_id)
    return decision
