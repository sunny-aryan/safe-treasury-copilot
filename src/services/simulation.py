from typing import Any, Dict

from src.data_loader import load_json


def get_prices() -> Dict[str, Any]:
    return load_json("prices.json")


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
            "slippage_bps": 35,
        }

    if from_token == "USDC" and to_token == "DAI":
        estimated_out = round(amount, 2)
        return {
            "success": True,
            "simulation_type": "swap",
            "estimated_output": estimated_out,
            "output_token": "DAI",
            "slippage_bps": 5,
        }

    return {
        "success": False,
        "reason": f"Unsupported swap pair: {from_token} -> {to_token}",
    }


def simulate_deposit(token: str, protocol: str, amount: float) -> Dict[str, Any]:
    return {
        "success": True,
        "simulation_type": "deposit",
        "protocol": protocol,
        "token": token,
        "amount": amount,
        "estimated_status": "funds_deposited",
    }


def simulate_transfer(token: str, wallet_name: str, amount: float) -> Dict[str, Any]:
    return {
        "success": True,
        "simulation_type": "transfer",
        "wallet_name": wallet_name,
        "token": token,
        "amount": amount,
        "estimated_status": "transfer_prepared",
    }
