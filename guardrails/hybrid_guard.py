import os

from guardrails.input_guard import check_input
from guardrails.mock_llm_guard import classify_prompt as classify_mock_prompt
from guardrails.policy import apply_risk_policy


LLM_MODE = os.getenv("GUARDEVAL_LLM_MODE", "mock").lower()


def _classify_semantically(prompt: str) -> dict:
    """
    Select the semantic guard implementation.

    mock:
        Deterministic local classifier for tests/CI.

    real:
        OpenAI-backed semantic classifier.
    """

    if LLM_MODE == "mock":
        result = classify_mock_prompt(prompt)
        result["method"] = "mock_llm"
        return result

    if LLM_MODE == "real":
        # Lazy import keeps mock/CI mode independent of OpenAI credentials.
        from guardrails.llm_guard import classify_prompt

        result = classify_prompt(prompt)
        result["method"] = "llm"
        return result

    raise ValueError(
        "GUARDEVAL_LLM_MODE must be either 'real' or 'mock'. "
        f"Got: {LLM_MODE!r}"
    )


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

    semantic_result = _classify_semantically(prompt)

    result = {
        "action": semantic_result["action"],
        "risk": semantic_result["risk"],
        "category": semantic_result["category"],
        "reason": semantic_result["reason"],
        "method": semantic_result["method"],
        "layers": [
            "rules",
            semantic_result["method"],
            "policy",
        ],
    }

    return apply_risk_policy(result)
