# Trade-offs

## Why proposal generation instead of execution

Safe Treasury Copilot intentionally creates proposals rather than executing transactions.

This reduces operational risk and keeps humans in the approval loop for sensitive treasury actions. The trade-off is that the system demonstrates decision support rather than end-to-end transaction automation.

## Why deterministic policy enforcement

The LLM is used for intent parsing, but policy decisions are deterministic.

This avoids giving the LLM authority over safety-critical decisions such as whether a transfer is allowed, whether approval is required, or whether a destination is trusted.

## Why synthetic treasury data

The prototype uses synthetic balances, prices, policies, and service health states.

This makes the project safe, reproducible, and easy to run locally. The trade-off is that it does not reflect real-time market conditions, wallet state, or protocol-specific execution constraints.

## Why an explainable risk model

The risk model is intentionally simple and transparent.

It uses factors such as amount, action type, destination allowlist status, and protocol or wallet risk level. This makes the decision path easy to inspect, but it is not a real financial risk model.

## Why Streamlit

Streamlit enables rapid prototyping and makes the workflow easy to demo.

The trade-off is that it is not designed here as a production-grade treasury operations interface with authentication, role-based access control, or persistent workflow state.

## Why service degradation is simulated

The app includes service health toggles to show how the system behaves when dependencies degrade.

This helps demonstrate failure-aware product design without requiring real indexers, simulation APIs, or transaction services.

## What this system does not solve

This prototype does not include:

- real wallet execution
- authentication or user permissions
- persistent proposal history
- real protocol integrations
- production observability
- compliance workflows
- multi-signer approval routing

These are intentionally out of scope for the first version.