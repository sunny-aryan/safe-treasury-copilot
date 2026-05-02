import json
from pathlib import Path
from typing import Any, Dict

DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def load_json(filename: str) -> Dict[str, Any]:
    with open(DATA_DIR / filename, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(filename: str, data: Dict[str, Any]) -> None:
    with open(DATA_DIR / filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_treasury() -> Dict[str, Any]:
    return load_json("treasury.json")


def get_policies() -> Dict[str, Any]:
    return load_json("policies.json")


def get_prices() -> Dict[str, Any]:
    return load_json("prices.json")


def get_service_health() -> Dict[str, Any]:
    return load_json("service_health.json")


def set_service_health(indexer: str, simulation_service: str, tx_service: str) -> None:
    save_json(
        "service_health.json",
        {
            "indexer": indexer,
            "simulation_service": simulation_service,
            "tx_service": tx_service,
        },
    )


def get_balance(token: str) -> float:
    treasury = get_treasury()
    return treasury["balances"].get(token, 0)


def simulate_swap(from_token: str, to_token: str, amount: float) -> Dict[str, Any]:
    prices = get_prices()

    if from_token == "USDC" and to_token == "ETH":
        eth_price = prices["ETH_USDC"]
        estimated_out = round(amount / eth_price, 6)
        return {
            "success": True,
            "simulation_type": "swap",
            "estimated_output": estimated_out,
            "output_token": "ETH",
            "slippage_bps": 35
        }

    if from_token == "USDC" and to_token == "DAI":
        estimated_out = round(amount, 2)
        return {
            "success": True,
            "simulation_type": "swap",
            "estimated_output": estimated_out,
            "output_token": "DAI",
            "slippage_bps": 5
        }

    return {
        "success": False,
        "reason": f"Unsupported swap pair: {from_token} -> {to_token}"
    }


def simulate_deposit(token: str, protocol: str, amount: float) -> Dict[str, Any]:
    return {
        "success": True,
        "simulation_type": "deposit",
        "protocol": protocol,
        "token": token,
        "amount": amount,
        "estimated_status": "funds_deposited"
    }


def simulate_transfer(token: str, wallet_name: str, amount: float) -> Dict[str, Any]:
    return {
        "success": True,
        "simulation_type": "transfer",
        "wallet_name": wallet_name,
        "token": token,
        "amount": amount,
        "estimated_status": "transfer_prepared"
    }


def create_proposal(action_payload: Dict[str, Any], simulation: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "proposal_id": "proposal_001",
        "status": "created",
        "human_approval_required": True,
        "payload": action_payload,
        "simulation_summary": simulation
    }
