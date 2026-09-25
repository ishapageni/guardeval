
from guardrails.hybrid_guard import hybrid_check
from guardrails.tool_guard import check_tool_call
from guardrails.output_guard import check_output


def process_request(
    prompt: str,
    proposed_tool: dict | None = None,
    generated_output: str | None = None,
) -> dict:
    """
    End-to-end guarded agent pipeline.

    Flow:
        Input → Guard → Agent → Tool Guard → Output Guard
    """

    # -------------------------------------------------
    # 1. Input guard
    # -------------------------------------------------

    input_result = hybrid_check(prompt)

    if input_result["policy_action"] == "block":
        return {
            "final_action": "block",
            "stage": "input_guard",
            "reason": input_result["reason"],
            "risk": input_result["risk"],
        }

    if input_result["policy_action"] == "review":
        return {
            "final_action": "review",
            "stage": "input_guard",
            "reason": input_result["reason"],
            "risk": input_result["risk"],
        }

    # -------------------------------------------------
    # 2. Tool-call guard
    # -------------------------------------------------

    if proposed_tool is not None:

        tool_name = proposed_tool["name"]
        arguments = proposed_tool.get("arguments", {})

        tool_result = check_tool_call(
            tool_name,
            arguments
        )

        if tool_result["action"] == "block":
            return {
                "final_action": "block",
                "stage": "tool_guard",
                "tool": tool_name,
                "reason": tool_result["reason"],
                "risk": tool_result["risk"],
            }

        if tool_result["action"] == "review":
            return {
                "final_action": "review",
                "stage": "tool_guard",
                "tool": tool_name,
                "reason": tool_result["reason"],
                "risk": tool_result["risk"],
            }

    # -------------------------------------------------
    # 3. Output guard
    # -------------------------------------------------

    if generated_output is not None:

        output_result = check_output(generated_output)

        if output_result["action"] == "block":
            return {
                "final_action": "block",
                "stage": "output_guard",
                "reason": output_result["reason"],
                "risk": output_result["risk"],
            }

        if output_result["action"] == "review":
            return {
                "final_action": "review",
                "stage": "output_guard",
                "reason": output_result["reason"],
                "risk": output_result["risk"],
            }

    # -------------------------------------------------
    # 4. Everything passed
    # -------------------------------------------------

    return {
        "final_action": "allow",
        "stage": "agent",
        "reason": "Request passed all configured guardrails",
        "risk": 0.05,
    }
