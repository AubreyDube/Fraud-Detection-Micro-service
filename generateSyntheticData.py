# tools/generate_synthetic_events.py
import json, random, uuid, datetime as dt
from faker import Faker
import ulid

fake = Faker()
CURRENCIES = ["ZAR", "USD", "GBP"]
CHANNELS   = ["mobile", "web", "ecom", "pos"]
STATUS     = ["authorised", "declined", "reversed", "pending"]

def make_event():
    now = dt.datetime.utcnow().replace(microsecond=0)
    amt = round(random.uniform(10, 5000), 2)
    return {
        "event_id": str(ulid.new()),
        "event_time": now.isoformat() + "Z",
        "event_type": "transaction",
        "schema_version": "1.0.0",
        "transaction": {
            "transaction_id": f"TX-{uuid.uuid4().hex[:8]}",
            "account_id": fake.uuid4(),
            "timestamp": now.isoformat() + "Z",
            "amount": amt,
            "currency": random.choice(CURRENCIES),
            "merchant": {
                "mcc": f"{random.randint(4000, 5999)}",
                "merchant_id": fake.uuid4(),
                "name": fake.company()
            },
            "channel": random.choice(CHANNELS),
            "status": random.choice(STATUS)
        },
        "device": {
            "device_id": fake.uuid4(),
            "ip_address": fake.ipv4_public(),
            "user_agent": fake.user_agent(),
            "fingerprint": fake.md5()
        },
        "location": {
            "lat": float(fake.latitude()),
            "lon": float(fake.longitude()),
            "country_iso": "ZA",
            "region": "Gauteng",
            "city": "Johannesburg"
        },
        "features": {
            "is_high_risk_country": False,
            "minutes_since_last_tx": random.randint(1, 60),
            "velocity_score": round(random.random(), 2),
            "historical_avg_amount": round(amt * random.uniform(0.6, 1.4), 2)
        },
        "pii_redacted": True,
        "consent_flags": ["fraud_scoring_v1"]
    }

if __name__ == "__main__":
    import sys, gzip
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    with gzip.open("synthetic_events.json.gz", "wt") as f:
        for _ in range(n):
            f.write(json.dumps(make_event()) + "\n")
