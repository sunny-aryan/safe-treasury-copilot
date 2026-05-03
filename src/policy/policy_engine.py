from typing import Dict, List


def evaluate_policy(intent: Dict, policies: Dict) -> Dict:
    approval_reasons: List[str] = []
    blocking_reasons: List[str] = []

    action = intent.get("action")

    if action == "swap_asset":
        amount = float(intent.get("amount", 0))

        if amount > policies["max_swap_without_manual_review"]:
            approval_reasons.append("Swap amount exceeds auto-review threshold.")

    elif action == "deposit_protocol":
        protocol = intent.get("protocol")
        amount = float(intent.get("amount", 0))

        if protocol not in policies["allowlisted_protocols"]:
            blocking_reasons.append(f"Protocol '{protocol}' is not allowlisted.")

        if amount > policies.get("max_protocol_deposit_without_manual_review", 15000):
            approval_reasons.append("Deposit amount exceeds auto-review threshold.")

    elif action == "transfer_wallet":
        wallet = intent.get("wallet_name")

        if wallet not in policies["allowlisted_wallets"]:
            blocking_reasons.append(f"Wallet '{wallet}' is not allowlisted.")

    else:
        blocking_reasons.append(f"Unsupported action type: {action}")

    if blocking_reasons:
        return {
            "decision": "blocked",
            "approval_tier": None,
            "approval_required": False,
            "blocking_reasons": blocking_reasons,
            "approval_reasons": approval_reasons,
            "reasons": blocking_reasons + approval_reasons,
        }

    if approval_reasons:
        return {
            "decision": "requires_approval",
            "approval_tier": "manual_review",
            "approval_required": True,
            "blocking_reasons": [],
            "approval_reasons": approval_reasons,
            "reasons": approval_reasons,
        }

    return {
        "decision": "pass",
        "approval_tier": "auto_proposal",
        "approval_required": False,
        "blocking_reasons": [],
        "approval_reasons": [],
        "reasons": [],
    }
