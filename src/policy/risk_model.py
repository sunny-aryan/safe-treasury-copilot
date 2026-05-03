from typing import Any, Dict, List


RISK_LEVEL_POINTS = {
    "low": 10,
    "medium": 25,
    "high": 50,
    "unknown": 75,
}


def get_amount_risk(
    action: str,
    amount: float,
    policies: Dict[str, Any],
) -> Dict[str, Any]:
    thresholds = policies.get("amount_thresholds", {}).get(action, {})

    manual_review_threshold = thresholds.get("manual_review")
    multi_sig_threshold = thresholds.get("multi_sig_required")

    if multi_sig_threshold is not None and amount > multi_sig_threshold:
        return {
            "points": 60,
            "factor": f"Amount {amount} exceeds multi-sig threshold of {multi_sig_threshold}.",
            "approval_tier": "multi_sig_required",
        }

    if manual_review_threshold is not None and amount > manual_review_threshold:
        return {
            "points": 30,
            "factor": f"Amount {amount} exceeds manual review threshold of {manual_review_threshold}.",
            "approval_tier": "manual_review",
        }

    return {
        "points": 5,
        "factor": "Amount is within auto-proposal threshold.",
        "approval_tier": "auto_proposal",
    }


def get_destination_risk(intent: Dict[str, Any], policies: Dict[str, Any]) -> Dict[str, Any]:
    action = intent.get("action")

    if action == "deposit_protocol":
        protocol = intent.get("protocol")
        protocol_policy = policies.get("protocols", {}).get(protocol)

        if not protocol_policy:
            return {
                "points": 75,
                "factor": f"Protocol '{protocol}' is unknown.",
                "allowlisted": False,
                "approval_tier": "blocked",
            }

        risk_level = protocol_policy.get("risk_level", "unknown")

        return {
            "points": RISK_LEVEL_POINTS.get(risk_level, 75),
            "factor": f"Protocol '{protocol}' has {risk_level} risk.",
            "allowlisted": protocol_policy.get("allowlisted", False),
            "approval_tier": "auto_proposal",
        }

    if action == "transfer_wallet":
        wallet = intent.get("wallet_name")
        wallet_policy = policies.get("wallets", {}).get(wallet)

        if not wallet_policy:
            return {
                "points": 75,
                "factor": f"Wallet '{wallet}' is unknown.",
                "allowlisted": False,
                "approval_tier": "blocked",
            }

        risk_level = wallet_policy.get("risk_level", "unknown")

        return {
            "points": RISK_LEVEL_POINTS.get(risk_level, 75),
            "factor": f"Wallet '{wallet}' has {risk_level} risk.",
            "allowlisted": wallet_policy.get("allowlisted", False),
            "approval_tier": "auto_proposal",
        }

    if action == "swap_asset":
        return {
            "points": 10,
            "factor": "Swap action has standard execution risk.",
            "allowlisted": True,
            "approval_tier": "auto_proposal",
        }

    return {
        "points": 75,
        "factor": f"Unsupported action '{action}'.",
        "allowlisted": False,
        "approval_tier": "blocked",
    }


def calculate_risk(intent: Dict[str, Any], policies: Dict[str, Any]) -> Dict[str, Any]:
    action = intent.get("action")
    amount = float(intent.get("amount", 0))

    risk_factors: List[str] = []

    amount_risk = get_amount_risk(action, amount, policies)
    destination_risk = get_destination_risk(intent, policies)

    risk_score = amount_risk["points"] + destination_risk["points"]

    risk_factors.append(amount_risk["factor"])
    risk_factors.append(destination_risk["factor"])

    approval_tier = "auto_proposal"

    if (
        amount_risk["approval_tier"] == "multi_sig_required"
        or risk_score >= 80
    ):
        approval_tier = "multi_sig_required"
    elif (
        amount_risk["approval_tier"] == "manual_review"
        or risk_score >= 40
    ):
        approval_tier = "manual_review"

    return {
        "risk_score": risk_score,
        "risk_factors": risk_factors,
        "destination_allowlisted": destination_risk["allowlisted"],
        "approval_tier": approval_tier,
    }
