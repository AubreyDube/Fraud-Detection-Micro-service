from pathlib import Path
import json
import jsonschema
import pytest

SCHEMA_PATH = Path("eventSchema.json")
SCHEMA = json.loads(SCHEMA_PATH.read_text())
RESOLVER = jsonschema.RefResolver(base_uri=SCHEMA_PATH.resolve().as_uri(), referrer=SCHEMA)


def validate_event(event):
    jsonschema.Draft202012Validator(SCHEMA, resolver=RESOLVER).validate(event)


def valid_event():
    return {
        "event_id": "01ARZ3NDEKTSV4RRFFQ69G5FAV",
        "event_time": "2024-01-01T00:00:00Z",
        "event_type": "transaction",
        "schema_version": "1.0.0",
        "transaction": {
            "transaction_id": "TX-12345678",
            "account_id": "acc-123",
            "timestamp": "2024-01-01T00:00:00Z",
            "amount": 100.0,
            "currency": "USD",
            "merchant": {
                "mcc": "1234",
                "merchant_id": "merch-1",
                "name": "Store"
            },
            "channel": "ecom",
            "status": "authorised"
        },
        "device": {
            "device_id": "dev-1",
            "ip_address": "192.168.1.1",
            "user_agent": "Mozilla/5.0",
            "fingerprint": "abc"
        },
        "location": {
            "lat": 0,
            "lon": 0,
            "country_iso": "US",
            "region": "CA",
            "city": "San Francisco"
        },
        "features": {
            "is_high_risk_country": False,
            "minutes_since_last_tx": 10,
            "velocity_score": 0.5,
            "historical_avg_amount": 120.0
        },
        "pii_redacted": False,
        "consent_flags": ["fraud_scoring_v1"]
    }


def test_valid_event_passes_schema():
    event = valid_event()
    validate_event(event)


def test_malformed_event_rejected_by_schema():
    event = valid_event()
    # Introduce an invalid channel value not allowed by the schema
    event["transaction"]["channel"] = "invalid_channel"
    with pytest.raises(jsonschema.ValidationError):
        validate_event(event)
