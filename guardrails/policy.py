
def apply_risk_policy(result: dict) -> dict:
    """
    Convert a numerical risk score into an enforcement action.

    < 0.30  -> allow
    0.30-0.69 -> review
    >= 0.70 -> block
    """

    risk = float(result.get("risk", 1.0))

    if risk >= 0.70:
        action = "block"
    elif risk >= 0.30:
        action = "review"
    else:
        action = "allow"

    return {
        **result,
        "policy_action": action,
    }
