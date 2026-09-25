
import re


SENSITIVE_OUTPUT_PATTERNS = [
    r"system prompt",
    r"hidden instructions",
    r"confidential initialization",
    r"private customer",
    r"customer'?s private information",
    r"customer records",
    r"private records",
    r"confidential customer",
    r"password",
    r"api key",
    r"secret key",
]


def check_output(output: str) -> dict:
    """
    Inspect generated agent output before returning it to the user.
    """

    text = output.lower().strip()

    for pattern in SENSITIVE_OUTPUT_PATTERNS:
        if re.search(pattern, text):
            return {
                "action": "block",
                "risk": 0.95,
                "category": "sensitive_output",
                "reason": "Potentially sensitive information detected in output",
            }

    return {
        "action": "allow",
        "risk": 0.05,
        "category": "safe_output",
        "reason": "No sensitive output pattern detected",
    }
