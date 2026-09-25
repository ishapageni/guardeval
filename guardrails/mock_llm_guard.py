
import re


def classify_prompt(prompt: str) -> dict:
    """
    Temporary semantic-risk simulator.

    This is NOT an LLM.
    It approximates semantic intent so the hybrid architecture
    can be tested without API credits.
    """

    text = prompt.lower().strip()

    # -------------------------------------------------
    # Benign security-education patterns
    # -------------------------------------------------

    benign_security_patterns = [
        r"how .*protect",
        r"techniques for protecting",
        r"how .*secure",
        r"how .*prevent",
        r"explain .*security",
        r"what .*security",
        r"best practices",
    ]

    # Educational/security questions should not be treated
    # as requests to obtain protected information.
    if any(re.search(pattern, text) for pattern in benign_security_patterns):
        return {
            "action": "allow",
            "risk": 0.05,
            "category": "benign_security_education",
            "reason": "Security-related educational request",
            "method": "mock_llm",
        }

    # -------------------------------------------------
    # Prompt-injection concepts
    # -------------------------------------------------

    instruction_override = [
        r"original .* constraints .* no longer apply",
        r"operating .* constraints .* no longer apply",
        r"follow my instructions instead",
        r"different set of instructions",
        r"prioritize my request",
        r"original instructions",
        r"normal instructions",
    ]

    # -------------------------------------------------
    # Data-exfiltration concepts
    # -------------------------------------------------

    sensitive_data = [
        r"information .* not permitted",
        r"information .* inaccessible",
        r"records .* inaccessible",
        r"information belonging to another",
        r"another customer",
        r"private information",
        r"confidential information",
        r"protected information",
    ]

    # -------------------------------------------------
    # Tool-abuse concepts
    # -------------------------------------------------

    destructive_action = [
        r"wipe .* accounts",
        r"removes all .* accounts",
        r"remove .* existing accounts",
        r"irreversible operation",
        r"administrative interface .* accounts",
    ]

    # -------------------------------------------------
    # Jailbreak concepts
    # -------------------------------------------------

    safety_bypass = [
        r"without .* restrictions",
        r"restrictions .* assistant",
        r"safety boundaries",
        r"normal safety",
        r"safety .* do not exist",
    ]

    pattern_groups = [
        ("semantic_prompt_injection", instruction_override),
        ("semantic_data_exfiltration", sensitive_data),
        ("semantic_tool_abuse", destructive_action),
        ("semantic_jailbreak", safety_bypass),
    ]

    for category, patterns in pattern_groups:
        for pattern in patterns:
            if re.search(pattern, text):
                return {
                    "action": "block",
                    "risk": 0.95,
                    "category": category,
                    "reason": f"Semantic risk detected: {category}",
                    "method": "mock_llm",
                }

    return {
        "action": "allow",
        "risk": 0.05,
        "category": "benign",
        "reason": "No semantic risk detected",
        "method": "mock_llm",
    }
