from src.policy.risk_model import calculate_risk


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


def test_low_risk_swap_gets_auto_proposal_tier():
    intent = {
        "action": "swap_asset",
        "from_token": "USDC",
        "to_token": "ETH",
        "amount": 5000,
    }

    result = calculate_risk(intent, POLICIES)

    assert result["risk_score"] == 15
    assert result["approval_tier"] == "auto_proposal"
    assert result["destination_allowlisted"] is True


def test_large_allowlisted_deposit_gets_manual_review_tier():
    intent = {
        "action": "deposit_protocol",
        "token": "USDC",
        "protocol": "Aave",
        "amount": 20000,
    }

    result = calculate_risk(intent, POLICIES)

    assert result["risk_score"] == 40
    assert result["approval_tier"] == "manual_review"
    assert result["destination_allowlisted"] is True


def test_unknown_protocol_is_not_allowlisted():
    intent = {
        "action": "deposit_protocol",
        "token": "USDC",
        "protocol": "UnknownProtocol",
        "amount": 10000,
    }

    result = calculate_risk(intent, POLICIES)

    assert result["risk_score"] == 80
    assert result["approval_tier"] == "multi_sig_required"
    assert result["destination_allowlisted"] is False


def test_very_large_swap_gets_multi_sig_tier():
    intent = {
        "action": "swap_asset",
        "from_token": "USDC",
        "to_token": "ETH",
        "amount": 60000,
    }

    result = calculate_risk(intent, POLICIES)

    assert result["approval_tier"] == "multi_sig_required"
    assert result["destination_allowlisted"] is True
    assert result["risk_score"] >= 70
