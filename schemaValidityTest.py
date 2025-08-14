from pathlib import Path
import json
import jsonschema
import pytest

SCHEMA = json.loads(Path("eventSchema.json").read_text())
DATA_DIR = Path("tests/data")

def _load_events(pattern: str):
    return [json.loads(path.read_text()) for path in DATA_DIR.glob(pattern)]

@pytest.mark.parametrize("event", _load_events("valid*.json"))
def test_valid_events(event):
    jsonschema.validate(instance=event, schema=SCHEMA)

@pytest.mark.parametrize("event", _load_events("invalid*.json"))
def test_invalid_events(event):
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=event, schema=SCHEMA)
