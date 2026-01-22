import json
from pathlib import Path

FIXTURE_PATH = Path(__file__).with_name("sample_logs.json")

def load_sample_logs() -> list[dict]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))