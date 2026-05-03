from typing import Any, Dict


def create_proposal(action_payload: Dict[str, Any], simulation: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "proposal_id": "proposal_001",
        "status": "created",
        "human_approval_required": True,
        "payload": action_payload,
        "simulation_summary": simulation,
    }
