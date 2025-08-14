import sys
import pathlib
import json
import logging
import uuid

import jsonschema
import pytest

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

import fraud_detector
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
    expected = len(decision["reasons"]) / len(fraud_detector._RULES)
    assert decision["score"] == pytest.approx(expected)

def test_clean_transaction_passes():
    event = _base_event()
    decision = evaluate_transaction(event)
    assert decision == {"fraud": False, "score": 0.0, "reasons": []}


def test_invalid_event_raises():
    event = _base_event()
    event.pop("transaction")
    with pytest.raises(jsonschema.ValidationError):
        evaluate_transaction(event)


def test_multiple_flags_scaled_score():
    event = _base_event(
        transaction={"amount": 2000},
        features={"velocity_score": 0.9, "is_high_risk_country": False},
    )
    decision = evaluate_transaction(event)
    assert len(decision["reasons"]) == 2
    expected = len(decision["reasons"]) / len(fraud_detector._RULES)
    assert decision["score"] == pytest.approx(expected)


def test_valid_correlation_id_used(caplog):
    event = _base_event()
    cid = str(uuid.uuid4())
    with caplog.at_level(logging.INFO, logger="fraud_detector"):
        evaluate_transaction(event, correlation_id=cid)
    record = caplog.records[-1]
    assert json.loads(record.message)["correlation_id"] == cid


def test_invalid_correlation_id_replaced(caplog, monkeypatch):
    event = _base_event()
    new_cid = "00000000-0000-0000-0000-000000000001"
    monkeypatch.setattr("fraud_detector.uuid.uuid4", lambda: uuid.UUID(new_cid))
    with caplog.at_level(logging.INFO, logger="fraud_detector"):
        evaluate_transaction(event, correlation_id="not-a-uuid")
    record = caplog.records[-1]
    assert json.loads(record.message)["correlation_id"] == new_cid
