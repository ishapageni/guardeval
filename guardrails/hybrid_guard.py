
from guardrails.input_guard import check_input
from guardrails.mock_llm_guard import classify_prompt
from guardrails.policy import apply_risk_policy


def hybrid_check(prompt: str) -> dict:

    # ---------------------------------------------
    # Layer 1: deterministic rule guard
    # ---------------------------------------------

    rule_result = check_input(prompt)

    if rule_result["action"] == "block":
        result = {
            "action": "block",
            "risk": rule_result["risk"],
            "category": "rule_detected",
            "reason": rule_result["reason"],
            "method": "rules",
        }

        return apply_risk_policy(result)

    # ---------------------------------------------
    # Layer 2: semantic guard
    # ---------------------------------------------

    semantic_result = classify_prompt(prompt)

    result = {
        "action": semantic_result["action"],
        "risk": semantic_result["risk"],
        "category": semantic_result["category"],
        "reason": semantic_result["reason"],
        "method": "semantic",
    }

    return apply_risk_policy(result)
