import sys
import pathlib

import jsonschema
import pytest

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from fraud_detector import evaluate_transaction

def _base_event(**overrides):
    event = {
        "event_id": "1",
        "event_time": "2024-01-01T00:00:00Z",
        "transaction": {
            "transaction_id": "tx1",
            "account_id": "acct1",
            "timestamp": "2024-01-01T00:00:00Z",
            "amount": 50,
            "currency": "USD",
            "status": "authorised",
        },
        "features": {"velocity_score": 0.1, "is_high_risk_country": False},
    }
    for key, value in overrides.items():
        if key in event and isinstance(event[key], dict) and isinstance(value, dict):
            event[key].update(value)
        else:
            event[key] = value
    return event

def test_high_amount_flagged():
    event = _base_event(transaction={"amount": 2000})
    decision = evaluate_transaction(event)
    assert decision["fraud"]
    assert "amount_gt_1000" in decision["reasons"]

def test_clean_transaction_passes():
    event = _base_event()
    decision = evaluate_transaction(event)
    assert decision == {"fraud": False, "score": 0.0, "reasons": []}


def test_invalid_event_raises():
    event = _base_event()
    event.pop("transaction")
    with pytest.raises(jsonschema.ValidationError):
        evaluate_transaction(event)
