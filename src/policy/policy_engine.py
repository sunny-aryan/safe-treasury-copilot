from typing import Dict, List

from src.policy.risk_model import calculate_risk


def evaluate_policy(intent: Dict, policies: Dict) -> Dict:
    blocking_reasons: List[str] = []

    risk_result = calculate_risk(intent, policies)

    if not risk_result["destination_allowlisted"]:
        blocking_reasons.append("Destination is not allowlisted.")

    if blocking_reasons:
        return {
            "decision": "blocked",
            "approval_tier": None,
            "approval_required": False,
            "risk_score": risk_result["risk_score"],
            "risk_factors": risk_result["risk_factors"],
            "blocking_reasons": blocking_reasons,
            "approval_reasons": [],
            "reasons": blocking_reasons,
        }

    approval_tier = risk_result["approval_tier"]

    if approval_tier == "multi_sig_required":
        approval_reasons = [
            "Risk score requires multi-signature approval."
        ]

        return {
            "decision": "requires_approval",
            "approval_tier": "multi_sig_required",
            "approval_required": True,
            "risk_score": risk_result["risk_score"],
            "risk_factors": risk_result["risk_factors"],
            "blocking_reasons": [],
            "approval_reasons": approval_reasons,
            "reasons": approval_reasons,
        }

    if approval_tier == "manual_review":
        approval_reasons = [
            "Risk score requires manual review."
        ]

        return {
            "decision": "requires_approval",
            "approval_tier": "manual_review",
            "approval_required": True,
            "risk_score": risk_result["risk_score"],
            "risk_factors": risk_result["risk_factors"],
            "blocking_reasons": [],
            "approval_reasons": approval_reasons,
            "reasons": approval_reasons,
        }

    return {
        "decision": "pass",
        "approval_tier": "auto_proposal",
        "approval_required": False,
        "risk_score": risk_result["risk_score"],
        "risk_factors": risk_result["risk_factors"],
        "blocking_reasons": [],
        "approval_reasons": [],
        "reasons": [],
    }
