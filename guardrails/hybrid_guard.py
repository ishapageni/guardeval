import os

from guardrails.input_guard import check_input
from guardrails.llm_guard import classify_prompt as classify_real_prompt
from guardrails.mock_llm_guard import classify_prompt as classify_mock_prompt
from guardrails.policy import apply_risk_policy


LLM_MODE = os.getenv("GUARDEVAL_LLM_MODE", "mock").lower()


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
            "layers": ["rules", "policy"],
        }

        return apply_risk_policy(result)

    # ---------------------------------------------
    # Layer 2: semantic guard
    # ---------------------------------------------

    if LLM_MODE == "real":
        semantic_result = classify_real_prompt(prompt)
        semantic_method = "llm"
    elif LLM_MODE == "mock":
        semantic_result = classify_mock_prompt(prompt)
        semantic_method = "mock_llm"
    else:
        raise ValueError(
            "GUARDEVAL_LLM_MODE must be either 'real' or 'mock'."
        )

    result = {
        "action": semantic_result["action"],
        "risk": semantic_result["risk"],
        "category": semantic_result["category"],
        "reason": semantic_result["reason"],
        "method": semantic_method,
        "layers": ["rules", semantic_method, "policy"],
    }

    return apply_risk_policy(result)
