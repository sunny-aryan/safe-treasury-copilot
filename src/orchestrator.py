from typing import Dict, Any, List

from src.data_loader import get_policies
from src.parsing.llm_parser import parse_intent
from src.policy.policy_engine import evaluate_policy
from src.services.balances import get_balance
from src.services.health import get_service_health
from src.services.simulation import simulate_swap, simulate_deposit, simulate_transfer
from src.proposals.proposal_generator import create_proposal


def handle_request(user_input: str) -> Dict[str, Any]:
    audit: List[str] = []
    warnings: List[str] = []

    audit.append(f"User input: {user_input}")

    try:
        intent = parse_intent(user_input)
        audit.append(f"Parsed intent: {intent}")

        if intent.get("parser_mode") == "fallback_local":
            audit.append("LLM parser fallback used instead of OpenAI.")

        if intent.get("fallback_reason"):
            audit.append(f"Fallback reason: {intent['fallback_reason']}")

    except Exception as e:
        return {
            "status": "parse_error",
            "audit": audit + [f"Parser failed completely: {str(e)}"]
        }

    if intent["action"] == "clarification_needed":
        return {
            "status": "clarification_needed",
            "intent": intent,
            "audit": audit
        }

    policies = get_policies()
    health = get_service_health()
    audit.append(f"Service health: {health}")

    if health["indexer"] != "healthy":
        warnings.append("Indexer is degraded. Balances may be stale.")
        audit.append("Warning: Indexer degraded.")

    policy_result = evaluate_policy(intent, policies)
    audit.append(f"Policy result: {policy_result}")

    simulation = None

    if intent["action"] in ["swap_asset", "deposit_protocol", "transfer_wallet"]:
        if health["simulation_service"] != "healthy":
            return {
                "status": "blocked",
                "intent": intent,
                "policy_result": {
                    "allowed": False,
                    "status": "blocked",
                    "reasons": ["Simulation service is degraded; cannot safely prepare proposal."]
                },
                "warnings": warnings,
                "audit": audit
            }

    if intent["action"] == "swap_asset":
        balance = get_balance(intent["from_token"])
        audit.append(f"Balance check for {intent['from_token']}: {balance}")

        if balance < float(intent["amount"]):
            return {
                "status": "blocked",
                "intent": intent,
                "policy_result": {
                    "allowed": False,
                    "status": "blocked",
                    "reasons": ["Insufficient balance"]
                },
                "warnings": warnings,
                "audit": audit
            }

        simulation = simulate_swap(
            intent["from_token"],
            intent["to_token"],
            float(intent["amount"])
        )
        audit.append(f"Simulation result: {simulation}")

        if not simulation["success"]:
            return {
                "status": "blocked",
                "intent": intent,
                "policy_result": {
                    "allowed": False,
                    "status": "blocked",
                    "reasons": [simulation["reason"]]
                },
                "warnings": warnings,
                "audit": audit
            }

    elif intent["action"] == "deposit_protocol":
        balance = get_balance(intent["token"])
        audit.append(f"Balance check for {intent['token']}: {balance}")

        if balance < float(intent["amount"]):
            return {
                "status": "blocked",
                "intent": intent,
                "policy_result": {
                    "allowed": False,
                    "status": "blocked",
                    "reasons": ["Insufficient balance"]
                },
                "warnings": warnings,
                "audit": audit
            }

        simulation = simulate_deposit(
            intent["token"],
            intent["protocol"],
            float(intent["amount"])
        )
        audit.append(f"Simulation result: {simulation}")

    elif intent["action"] == "transfer_wallet":
        balance = get_balance(intent["token"])
        audit.append(f"Balance check for {intent['token']}: {balance}")

        if balance < float(intent["amount"]):
            return {
                "status": "blocked",
                "intent": intent,
                "policy_result": {
                    "allowed": False,
                    "status": "blocked",
                    "reasons": ["Insufficient balance"]
                },
                "warnings": warnings,
                "audit": audit
            }

        simulation = simulate_transfer(
            intent["token"],
            intent["wallet_name"],
            float(intent["amount"])
        )
        audit.append(f"Simulation result: {simulation}")

    if policy_result["decision"] == "blocked":
        audit.append("Request blocked by policy.")

        return {
            "status": "blocked",
            "intent": intent,
            "policy_result": policy_result,
            "simulation": simulation,
            "warnings": warnings,
            "audit": audit,
        }

    proposal = create_proposal(
        intent,
        simulation or {},
        policy_result=policy_result,
    )

    if policy_result["decision"] == "requires_approval":
        audit.append(f"Proposal created with approval requirement: {proposal}")

        return {
            "status": "human_approval_required",
            "intent": intent,
            "policy_result": policy_result,
            "simulation": simulation,
            "proposal": proposal,
            "warnings": warnings,
            "audit": audit,
        }

    audit.append(f"Proposal created: {proposal}")

    return {
        "status": "proposal_created",
        "intent": intent,
        "policy_result": policy_result,
        "simulation": simulation,
        "proposal": proposal,
        "warnings": warnings,
        "audit": audit,
    }
