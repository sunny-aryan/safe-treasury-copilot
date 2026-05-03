import json
from pathlib import Path
from typing import Any, Dict

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def load_json(filename: str) -> Dict[str, Any]:
    with open(DATA_DIR / filename, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(filename: str, data: Dict[str, Any]) -> None:
    with open(DATA_DIR / filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def get_policies() -> Dict[str, Any]:
    return load_json("policies.json")
