# tools/generate_synthetic_events.py
import json, uuid, datetime as dt, hashlib
from random import SystemRandom
from faker import Faker
from ulid import ULID

import jsonschema
from importlib import resources

SCHEMA = json.loads(resources.files("fraud_detector").joinpath("eventSchema.json").read_text())

fake = Faker()
rand = SystemRandom()
CURRENCIES = ["ZAR", "USD", "GBP"]
CHANNELS   = ["mobile", "web", "ecom", "pos"]
STATUS     = ["authorised", "declined", "reversed", "pending"]

def make_event():
    now = dt.datetime.utcnow().replace(microsecond=0)
    amt = round(rand.uniform(10, 5000), 2)
    event = {
        "event_id": str(ULID()),
        "event_time": now.isoformat() + "Z",
        "event_type": "transaction",
        "schema_version": "1.0.0",
        "transaction": {
            "transaction_id": f"TX-{uuid.uuid4().hex[:8]}",
            "account_id": fake.uuid4(),
            "timestamp": now.isoformat() + "Z",
            "amount": amt,
            "currency": rand.choice(CURRENCIES),
            "merchant": {
                "mcc": f"{rand.randint(4000, 5999)}",
                "merchant_id": fake.uuid4(),
                "name": fake.company()
            },
            "channel": rand.choice(CHANNELS),
            "status": rand.choice(STATUS)
        },
        "device": {
            "device_id": fake.uuid4(),
            "ip_address": fake.ipv4_public(),
            "user_agent": fake.user_agent(),
            "fingerprint": hashlib.sha256(fake.uuid4().encode()).hexdigest()
        },
        "location": {
            "lat": fake.latitude(),
            "lon": fake.longitude(),
            "country_iso": "ZA",
            "region": "Gauteng",
            "city": "Johannesburg"
        },
        "features": {
            "is_high_risk_country": False,
            "minutes_since_last_tx": rand.randint(1, 60),
            "velocity_score": round(rand.random(), 2),
            "historical_avg_amount": round(amt * rand.uniform(0.6, 1.4), 2)
        },
        "pii_redacted": True,
        "consent_flags": ["fraud_scoring_v1"]
    }
    jsonschema.validate(instance=event, schema=SCHEMA)
    return event

if __name__ == "__main__":
    import sys, gzip
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    with gzip.open("synthetic_events.json.gz", "wt") as f:
        for _ in range(n):
            f.write(json.dumps(make_event()) + "\n")
