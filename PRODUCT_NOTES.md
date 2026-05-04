# Product Notes

## Product framing

Safe Treasury Copilot is an AI-assisted decision-support tool for treasury operations.

It is designed to help a treasury operator convert natural-language requests into structured, auditable proposals while keeping policy enforcement deterministic and human-controlled.

The product intentionally avoids transaction execution. Its primary job is to prepare, validate, simulate, and route treasury actions for review.

## Target user

The primary user is a treasury operator, finance operations team member, or crypto treasury manager responsible for preparing asset movements such as:

- token swaps
- protocol deposits
- wallet transfers

These users need speed and clarity, but they also need strong controls because treasury mistakes can be costly and hard to reverse.

## User jobs to be done

### 1. Prepare a treasury action from natural language

When I describe a treasury action informally, I want the system to convert it into a structured request so that I do not need to manually fill out every field.

### 2. Understand whether the action is safe to propose

When I request a swap, deposit, or transfer, I want to know whether it passes policy, requires approval, or is blocked.

### 3. Create an auditable proposal

When a request is valid, I want a structured proposal that can be reviewed by a human approver.

### 4. Avoid unsafe guessing

When my request is ambiguous, I want the system to ask for clarification instead of making assumptions.

## Core product principles

1. **The LLM interprets, but does not approve.**  
   The LLM extracts intent from natural language. It does not decide whether an action is safe.

2. **Policy enforcement is deterministic.**  
   Approval requirements and blocked outcomes are controlled by explicit rules and risk logic.

3. **The system proposes, not executes.**  
   Treasury actions are prepared for review, not sent onchain.

4. **Ambiguity should stop the workflow.**  
   Missing amount, destination, or asset information should result in clarification.

5. **Degraded services should reduce system confidence.**  
   If simulation is unavailable, the system should not prepare a proposal.

## Key workflows

| Workflow | User input | Outcome |
|---|---|---|
| Low-risk swap | Convert 5000 USDC into ETH | Proposal created |
| Manual-review deposit | Deposit 20000 USDC into Aave | Human approval required |
| Blocked protocol | Deposit 10000 USDC into Compound | Blocked |
| Ambiguous request | Move some treasury funds into a safer asset | Clarification needed |
| Degraded simulation | Any simulatable action while simulation is degraded | Blocked |

## Success metrics

In a production version, I would evaluate the product using:

| Metric | Why it matters |
|---|---|
| Intent parsing success rate | Measures whether users can express requests naturally |
| Clarification rate | Indicates whether users are providing enough structured information |
| False approval rate | Critical safety metric; unsafe actions should not pass |
| False block rate | Measures whether policy is too restrictive |
| Proposal creation time | Measures operational efficiency |
| Human review completion time | Measures workflow usefulness after proposal generation |
| Service degradation handling rate | Measures resilience under dependency failures |

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| LLM misinterprets user intent | Use structured outputs, fallback parsing, and clarification flows |
| User over-trusts AI output | Make policy decisions explicit and auditable |
| Unsafe destination passes through | Use deterministic allowlists and blocked outcomes |
| Simulation unavailable | Block proposal creation when simulation is required |
| Risk score appears more precise than it is | Keep the model simple and explainable; document limitations |

## Scope decisions

### In scope

- natural-language intent parsing
- fallback parsing
- deterministic policy evaluation
- risk-based approval tiers
- synthetic treasury balances
- synthetic simulation
- service degradation behavior
- proposal JSON generation
- audit trail

### Out of scope

- real transaction execution
- real wallet integrations
- authentication
- role-based access control
- persistent proposal database
- real protocol risk feeds
- multi-signer approval workflow
- compliance review workflow

## Future product directions

Potential next iterations:

1. Add persistent proposal history and reviewer comments.
2. Add role-based approval workflows.
3. Add service degradation scenarios for stale balances and failed pricing.
4. Add multi-chain policy configuration.
5. Add gas fee simulation as a proposal field.
6. Add richer protocol risk metadata.
7. Add a lightweight reviewer dashboard.

## Product judgment

The main product decision was to keep the system focused on safe proposal generation rather than execution.

This makes the prototype narrower, but more credible. It demonstrates how AI can assist a high-risk workflow without replacing deterministic controls or human approval.