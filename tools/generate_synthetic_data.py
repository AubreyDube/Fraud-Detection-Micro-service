"""CLI utilities for generating synthetic transaction events."""

from __future__ import annotations

import argparse
import datetime as dt
import gzip
import hashlib
import json
import uuid
from pathlib import Path
from random import SystemRandom
from typing import Any, Sequence

from faker import Faker
# ULID generation
import ulid

import jsonschema

from fraud_detector.constants import CHANNELS, CURRENCIES, SCHEMA, STATUS

fake = Faker()
rand = SystemRandom()


def make_event() -> dict[str, Any]:
    """Generate a single synthetic transaction event.

    The returned dictionary conforms to :data:`fraud_detector.constants.SCHEMA`.

    Returns:
        A synthetic event dictionary.
    """

    now = dt.datetime.utcnow().replace(microsecond=0)
    amt = round(rand.uniform(10, 5000), 2)
    event: dict[str, Any] = {
        "event_id": str(ulid.new()),
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
                "name": fake.company(),
            },
            "channel": rand.choice(CHANNELS),
            "status": rand.choice(STATUS),
        },
        "device": {
            "device_id": fake.uuid4(),
            "ip_address": fake.ipv4_public(),
            "user_agent": fake.user_agent(),
            "fingerprint": hashlib.sha256(fake.uuid4().encode()).hexdigest(),
        },
        "location": {
            "lat": float(fake.latitude()),
            "lon": float(fake.longitude()),
            "country_iso": "ZA",
            "region": "Gauteng",
            "city": "Johannesburg",
        },
        "features": {
            "is_high_risk_country": False,
            "minutes_since_last_tx": rand.randint(1, 60),
            "velocity_score": round(rand.random(), 2),
            "historical_avg_amount": round(amt * rand.uniform(0.6, 1.4), 2),
        },
        "pii_redacted": True,
        "consent_flags": ["fraud_scoring_v1"],
    }
    jsonschema.validate(instance=event, schema=SCHEMA)
    return event


def main(argv: Sequence[str] | None = None) -> None:
    """CLI entry point for generating synthetic events.

    Args:
        argv: Optional sequence of arguments. If ``None``, ``sys.argv`` is used.
    """

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-n",
        "--num-events",
        type=int,
        default=1000,
        help="number of events to generate",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("synthetic_events.json.gz"),
        help="output gzip file",
    )
    args = parser.parse_args(argv)

    with gzip.open(args.output, "wt") as f:
        for _ in range(args.num_events):
            f.write(json.dumps(make_event()) + "\n")


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()

