from typing import Any, Dict

from src.data_loader import load_json


def get_treasury() -> Dict[str, Any]:
    return load_json("treasury.json")


def get_balance(token: str) -> float:
    treasury = get_treasury()
    return treasury["balances"].get(token, 0)
