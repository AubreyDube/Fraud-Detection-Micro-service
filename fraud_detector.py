import json
import logging
import uuid
from typing import Dict, Any

logger = logging.getLogger("fraud_detector")
_handler = logging.StreamHandler()
_handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(_handler)
logger.setLevel(logging.INFO)

def _log(entry: Dict[str, Any], correlation_id: str) -> None:
    log_record = {"correlation_id": correlation_id, **entry}
    logger.info(json.dumps(log_record))

def evaluate_transaction(event: Dict[str, Any], correlation_id: str | None = None) -> Dict[str, Any]:
    """Return fraud decision for a transaction event.

    Parameters
    ----------
    event: mapping conforming to the event schema
    correlation_id: optional ID used to correlate logs across services
    """
    correlation_id = correlation_id or str(uuid.uuid4())
    reasons = []
    tx = event.get("transaction", {})
    features = event.get("features", {})

    amount = tx.get("amount", 0)
    if amount > 1000:
        reasons.append("amount_gt_1000")

    if features.get("velocity_score", 0) > 0.8:
        reasons.append("velocity_score_high")

    if features.get("is_high_risk_country"):
        reasons.append("high_risk_country")

    is_fraud = bool(reasons)
    score = min(1.0, len(reasons) / 3)
    decision = {"fraud": is_fraud, "score": score, "reasons": reasons}

    _log({"event_id": event.get("event_id"), "decision": decision}, correlation_id)
    return decision
