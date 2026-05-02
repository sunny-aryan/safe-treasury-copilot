from typing import Dict, List


def evaluate_policy(intent: Dict, policies: Dict) -> Dict:
    reasons: List[str] = []
    action = intent.get("action")

    if action == "swap_asset":
        amount = float(intent.get("amount", 0))
        if amount > policies["max_swap_without_manual_review"]:
            reasons.append("Amount exceeds auto-review threshold.")

    if action == "deposit_protocol":
        protocol = intent.get("protocol")
        amount = float(intent.get("amount", 0))

        if protocol not in policies["allowlisted_protocols"]:
            reasons.append(f"Protocol '{protocol}' is not allowlisted.")

        if amount > policies.get("max_protocol_deposit_without_manual_review", 15000):
            reasons.append("Deposit exceeds auto-review threshold.")

    if action == "transfer_wallet":
        wallet = intent.get("wallet_name")
        if wallet not in policies["allowlisted_wallets"]:
            reasons.append(f"Wallet '{wallet}' is not allowlisted.")

    if reasons:
        return {
            "allowed": False,
            "status": "blocked",
            "reasons": reasons
        }

    return {
        "allowed": True,
        "status": "pass",
        "reasons": []
    }
