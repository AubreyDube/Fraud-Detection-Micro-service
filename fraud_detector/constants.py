import json
from importlib import resources

SCHEMA = json.loads(resources.files(__package__).joinpath("eventSchema.json").read_text())

CHANNELS = SCHEMA["properties"]["transaction"]["properties"]["channel"]["enum"]
STATUS = SCHEMA["properties"]["transaction"]["properties"]["status"]["enum"]
CURRENCIES = ["ZAR", "USD", "GBP"]

