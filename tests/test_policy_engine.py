from src.policy.policy_engine import evaluate_policy


POLICIES = {
    "amount_thresholds": {
        "swap_asset": {
            "manual_review": 10000,
            "multi_sig_required": 50000,
        },
        "deposit_protocol": {
            "manual_review": 15000,
            "multi_sig_required": 75000,
        },
        "transfer_wallet": {
            "manual_review": 10000,
            "multi_sig_required": 50000,
        },
    },
    "protocols": {
        "Aave": {
            "allowlisted": True,
            "risk_level": "low",
        },
        "Spark": {
            "allowlisted": True,
            "risk_level": "medium",
        },
        "Compound": {
            "allowlisted": False,
            "risk_level": "unknown",
        },
    },
    "wallets": {
        "operations_wallet": {
            "allowlisted": True,
            "risk_level": "low",
        },
        "payroll_wallet": {
            "allowlisted": True,
            "risk_level": "medium",
        },
    },
}


def test_low_risk_swap_passes_policy():
    intent = {
        "action": "swap_asset",
        "from_token": "USDC",
        "to_token": "ETH",
        "amount": 5000,
    }

    result = evaluate_policy(intent, POLICIES)

    assert result["decision"] == "pass"
    assert result["approval_tier"] == "auto_proposal"
    assert result["approval_required"] is False
    assert result["blocking_reasons"] == []


def test_large_allowlisted_deposit_requires_manual_review():
    intent = {
        "action": "deposit_protocol",
        "token": "USDC",
        "protocol": "Aave",
        "amount": 20000,
    }

    result = evaluate_policy(intent, POLICIES)

    assert result["decision"] == "requires_approval"
    assert result["approval_tier"] == "manual_review"
    assert result["approval_required"] is True
    assert result["blocking_reasons"] == []


def test_non_allowlisted_protocol_is_blocked():
    intent = {
        "action": "deposit_protocol",
        "token": "USDC",
        "protocol": "Compound",
        "amount": 10000,
    }

    result = evaluate_policy(intent, POLICIES)

    assert result["decision"] == "blocked"
    assert result["approval_required"] is False
    assert "Destination is not allowlisted." in result["blocking_reasons"]


def test_unknown_wallet_transfer_is_blocked():
    intent = {
        "action": "transfer_wallet",
        "token": "USDC",
        "wallet_name": "unknown_wallet",
        "amount": 2000,
    }

    result = evaluate_policy(intent, POLICIES)

    assert result["decision"] == "blocked"
    assert result["approval_required"] is False
    assert "Destination is not allowlisted." in result["blocking_reasons"]


def test_very_large_swap_requires_multi_sig():
    intent = {
        "action": "swap_asset",
        "from_token": "USDC",
        "to_token": "ETH",
        "amount": 60000,
    }

    result = evaluate_policy(intent, POLICIES)

    assert result["decision"] == "requires_approval"
    assert result["approval_tier"] == "multi_sig_required"
    assert result["approval_required"] is True
