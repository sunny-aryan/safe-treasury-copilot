from typing import Any, Dict, Optional


def create_proposal(
    action_payload: Dict[str, Any],
    simulation: Dict[str, Any],
    policy_result: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    policy_result = policy_result or {}

    return {
        "proposal_id": "proposal_001",
        "status": "created",
        "human_approval_required": policy_result.get("approval_required", True),
        "approval_tier": policy_result.get("approval_tier"),
        "policy_decision": policy_result.get("decision"),
        "policy_reasons": policy_result.get("reasons", []),
        "payload": action_payload,
        "simulation_summary": simulation,
    }
