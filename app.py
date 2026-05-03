import json
import streamlit as st

from src.orchestrator import handle_request
from src.services.health import get_service_health, set_service_health

st.set_page_config(page_title="Safe Treasury Copilot", layout="wide")
st.title("Safe Treasury Copilot (Prototype)")

st.write(
    "This prototype interprets treasury requests, checks policy, simulates outcomes, "
    "and creates a proposal requiring human approval."
)

st.sidebar.header("Service Health Controls")

current_health = get_service_health()

indexer_state = st.sidebar.selectbox(
    "Indexer status",
    ["healthy", "degraded"],
    index=0 if current_health["indexer"] == "healthy" else 1,
)

simulation_state = st.sidebar.selectbox(
    "Simulation service status",
    ["healthy", "degraded"],
    index=0 if current_health["simulation_service"] == "healthy" else 1,
)

tx_state = st.sidebar.selectbox(
    "Transaction service status",
    ["healthy", "degraded"],
    index=0 if current_health["tx_service"] == "healthy" else 1,
)

if st.sidebar.button("Apply service health"):
    set_service_health(indexer_state, simulation_state, tx_state)
    st.sidebar.success("Service health updated.")

sample_prompts = [
    "Convert 5000 USDC into ETH and prepare a proposal",
    "Deposit 10000 USDC into Aave and prepare a proposal",
    "Deposit 20000 USDC into Aave and prepare a proposal",
    "Deposit 10000 USDC into Compound and prepare a proposal",
    "Move some treasury funds into a safer asset",
    "Send 2000 USDC to operations_wallet and prepare a proposal"
]

selected = st.selectbox("Try a sample prompt", [""] + sample_prompts)

st.caption(
    "Use a sample prompt for quick testing, or enter any treasury request in natural language below."
)

user_input = st.text_area(
    "Enter treasury request",
    value=selected,
    height=120,
)

if st.button("Run"):
    if not user_input.strip():
        st.warning("Please enter a request.")
    else:
        result = handle_request(user_input)

        st.subheader("Final Status")
        st.write(result["status"])

        if "warnings" in result and result["warnings"]:
            st.subheader("Warnings")
            for warning in result["warnings"]:
                st.warning(warning)

        if "intent" in result:
            st.subheader("Parsed Intent")
            parser_mode = result["intent"].get("parser_mode", "unknown")

            if parser_mode == "openai":
                st.success("Parsed using OpenAI LLM")
            elif parser_mode == "fallback_local":
                st.warning("Parsed using fallback local parser")

            st.json(result["intent"])

        if "policy_result" in result:
            st.subheader("Policy Result")
            st.json(result["policy_result"])

        if "simulation" in result and result["simulation"] is not None:
            st.subheader("Simulation")
            st.json(result["simulation"])

        if "proposal" in result:
            st.subheader("Proposal")
            st.json(result["proposal"])

            proposal_str = json.dumps(result["proposal"], indent=2)

            st.download_button(
                label="Download proposal JSON",
                data=proposal_str,
                file_name="safe_proposal.json",
                mime="application/json"
            )

        st.subheader("Audit Trail")
        for line in result["audit"]:
            st.write("-", line)
