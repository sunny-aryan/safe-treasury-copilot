from typing import Any, Dict

from src.data_loader import load_json, save_json


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
