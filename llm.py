import json
import os
import re
from typing import Dict

from dotenv import load_dotenv

load_dotenv()

USE_OPENAI = bool(os.environ.get("OPENAI_API_KEY"))


def local_fallback_parse(user_input: str) -> Dict:
    text = user_input.strip()

    # 1) Swap asset
    # Example: "Convert 5000 USDC into ETH and prepare a proposal"
    swap_match = re.search(
        r"convert\s+(\d+(?:\.\d+)?)\s+([A-Za-z]+)\s+into\s+([A-Za-z]+)",
        text,
        re.IGNORECASE,
    )
    if swap_match:
        amount = float(swap_match.group(1))
        from_token = swap_match.group(2).upper()
        to_token = swap_match.group(3).upper()
        return {
            "action": "swap_asset",
            "from_token": from_token,
            "to_token": to_token,
            "amount": amount,
            "parser_mode": "fallback_local",
        }

    # 2) Deposit into protocol
    # Example: "Deposit 10000 USDC into Aave and prepare a proposal"
    deposit_match = re.search(
        r"deposit\s+(\d+(?:\.\d+)?)\s+([A-Za-z]+)\s+into\s+([A-Za-z]+)",
        text,
        re.IGNORECASE,
    )
    if deposit_match:
        amount = float(deposit_match.group(1))
        token = deposit_match.group(2).upper()
        protocol = deposit_match.group(3)
        return {
            "action": "deposit_protocol",
            "token": token,
            "protocol": protocol,
            "amount": amount,
            "parser_mode": "fallback_local",
        }

    # 3) Transfer to wallet
    # Example: "Send 2000 USDC to operations_wallet and prepare a proposal"
    transfer_match = re.search(
        r"send\s+(\d+(?:\.\d+)?)\s+([A-Za-z]+)\s+to\s+([A-Za-z_]+)",
        text,
        re.IGNORECASE,
    )
    if transfer_match:
        amount = float(transfer_match.group(1))
        token = transfer_match.group(2).upper()
        wallet_name = transfer_match.group(3)
        return {
            "action": "transfer_wallet",
            "token": token,
            "wallet_name": wallet_name,
            "amount": amount,
            "parser_mode": "fallback_local",
        }

    # 4) Clarification-needed case
    safer_match = re.search(r"safer asset|safely|safe asset", text, re.IGNORECASE)
    if safer_match:
        return {
            "action": "clarification_needed",
            "question": "How much would you like to move, and which safer asset do you have in mind?",
            "parser_mode": "fallback_local",
        }

    return {
        "action": "clarification_needed",
        "question": "I could not confidently parse that request. Please specify the action, amount, and destination asset or protocol.",
        "parser_mode": "fallback_local",
    }


def openai_parse(user_input: str) -> Dict:
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    system_prompt = """
You are an intent parser for a Safe-style onchain treasury assistant.

Return ONLY valid JSON.

Supported action types:
- swap_asset
- deposit_protocol
- transfer_wallet
- clarification_needed

Examples:

User: Convert 5000 USDC into ETH and prepare a proposal
Output:
{
  "action": "swap_asset",
  "from_token": "USDC",
  "to_token": "ETH",
  "amount": 5000
}

User: Deposit 10000 USDC into Aave and prepare a proposal
Output:
{
  "action": "deposit_protocol",
  "token": "USDC",
  "protocol": "Aave",
  "amount": 10000
}

User: Send 2000 USDC to operations_wallet and prepare a proposal
Output:
{
  "action": "transfer_wallet",
  "token": "USDC",
  "wallet_name": "operations_wallet",
  "amount": 2000
}

User: Move some treasury funds into a safer asset
Output:
{
  "action": "clarification_needed",
  "question": "How much would you like to move, and which safer asset do you have in mind?"
}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ],
    )

    parsed = json.loads(response.output_text)
    parsed["parser_mode"] = "openai"
    return parsed


def parse_intent(user_input: str) -> Dict:
    if not USE_OPENAI:
        return local_fallback_parse(user_input)

    try:
        return openai_parse(user_input)
    except Exception as e:
        fallback_result = local_fallback_parse(user_input)
        fallback_result["fallback_reason"] = str(e)
        return fallback_result
