from pathlib import Path
import json
from jsonschema import Draft202012Validator

SCHEMA = json.loads(Path("eventSchema.json").read_text())

def test_schema_is_valid():
    Draft202012Validator.check_schema(SCHEMA)
