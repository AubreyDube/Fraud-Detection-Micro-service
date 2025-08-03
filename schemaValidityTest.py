from pathlib import Path
import json, jsonschema, pytest

SCHEMA = json.loads(Path("eventSchema.json").read_text())

@pytest.fixture()
def example():
    return json.loads(Path("eventSchema.json").read_text())

def test_valid_event(example):
    jsonschema.validate(example, SCHEMA)
