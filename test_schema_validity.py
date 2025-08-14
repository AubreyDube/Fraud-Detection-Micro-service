from pathlib import Path
import json
import jsonschema

from generateSyntheticData import make_event


SCHEMA = json.loads(Path("eventSchema.json").read_text())


def test_generated_event_matches_schema():
    event = make_event()
    jsonschema.validate(event, SCHEMA)

