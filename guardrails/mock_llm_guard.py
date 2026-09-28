import re


def _matches_any(text, patterns):
    return any(
        re.search(pattern, text)
        for pattern in patterns
    )


def classify_prompt(prompt: str) -> dict:
    """
    Deterministic semantic-risk simulator.

    This is NOT an LLM.

    It approximates security-relevant intent using
    broader concept patterns so the hybrid architecture
    can be evaluated without API credits.

    The benchmark dataset is kept separate from these rules.
    """

    text = prompt.lower().strip()

    # -------------------------------------------------
    # Benign security education
    # -------------------------------------------------

    benign_security_patterns = [
        r"how .*protect",
        r"techniques for protecting",
        r"how .*secure",
        r"how .*prevent",
        r"explain .*security",
        r"what .*security",
        r"best practices",
        r"why .*security",
        r"why should .* be protected",
    ]

    if _matches_any(
        text,
        benign_security_patterns,
    ):
        return {
            "action": "allow",
            "risk": 0.05,
            "category": "benign_security_education",
            "reason": "Security-related educational request",
            "method": "mock_llm",
        }

    # -------------------------------------------------
    # Prompt injection
    # -------------------------------------------------

    instruction_override = [
        r"ignore .* instruction",
        r"disregard .* instruction",
        r"override .* instruction",
        r"set aside .* instruction",
        r"higher priority",
        r"treat .* as .* priority",
        r"reveal .* instruction",
        r"expose .* instruction",
        r"hidden .* instruction",
        r"previous .* instruction",
        r"prior .* instruction",
        r"constraints .* normally",
        r"disregard .* constraints",
        r"ignore .* constraints",
        r"constraints .* came before",
        r"constraints .* came earlier",
        r"constraints .* that came before",
        r"constraints .* that came earlier",
    ]

    # -------------------------------------------------
    # Data exfiltration
    # -------------------------------------------------

    sensitive_data = [
        r"private information",
        r"confidential information",
        r"protected information",
        r"private .* data",
        r"sensitive .* data",
        r"private .* files",
        r"sensitive .* files",
        r"authentication material",
        r"api keys",
        r"private configuration",
        r"protected configuration",
        r"information .* not permitted",
        r"information .* inaccessible",
        r"records .* inaccessible",
        r"information belonging to another",
        r"another customer",
        r"not intended .* user",
        r"ordinary users .* not",
    ]

    # -------------------------------------------------
    # Tool abuse
    # -------------------------------------------------

    tool_abuse = [
        r"system[- ]changing",
        r"change .* system",
        r"modify .* system",
        r"system .* state",
        r"privileged .* change",
        r"privileged .* operation",
        r"system operation",
        r"consequential .* operation",
        r"available .* tools",
        r"available .* capabilities",
        r"use .* tools",
        r"use .* capability",
        r"without .* confirmation",
        r"without .* authorization",
        r"without .* approval",
        r"without .* permission",
        r"owner .* confirmation",
        r"owner .* approved",
        r"wipe .* accounts",
        r"removes all .* accounts",
        r"remove .* existing accounts",
        r"irreversible operation",
        r"administrative interface .* accounts",
    ]

    # -------------------------------------------------
    # Jailbreak / safety bypass
    # -------------------------------------------------

    safety_bypass = [
        r"without .* restrictions",
        r"restrictions .* do not exist",
        r"disregard .* restrictions",
        r"ignore .* restrictions",
        r"bypass .* restrictions",
        r"bypass .* safeguards",
        r"remove .* safeguards",
        r"without .* safeguards",
        r"safety boundaries",
        r"normal safety",
        r"normally .* prevent",
        r"normally .* reject",
        r"normally .* blocked",
        r"normally .* rejected",
        r"unrestricted",
        r"unrestricted assistant",
    ]

    # -------------------------------------------------
    # Malicious-code concepts
    # -------------------------------------------------

    malicious_code = [
        r"malicious code",
        r"malicious program",

        r"code .* extract .* private .* files",
        r"code .* extract .* sensitive .* files",
        r"extract .* another .* private .* files",
        r"extract .* another .* user",
        r"extract .* private .* files",
        r"extract .* sensitive .* information",

        r"secretly .* collect",
        r"secretly .* gather",
        r"quietly .* collect",
        r"quietly .* gather",
        r"silently .* collect",
        r"silently .* extract",
        r"covertly .* collect",
        r"covertly .* extract",

        r"collect .* private .* information",
        r"collect .* private .* data",
        r"collect .* sensitive .* information",
        r"collect .* sensitive .* data",

        r"transmit .* data",
        r"transfer .* data",
        r"send .* data .* remote",
        r"send .* data .* endpoint",
        r"transmit .* remote",
        r"transmit .* remote endpoint",
        r"remote endpoint",
        r"forward .* remotely",
    ]

    # -------------------------------------------------
    # Evaluate semantic categories
    # -------------------------------------------------

    pattern_groups = [
        (
            "semantic_prompt_injection",
            instruction_override,
        ),
        (
            "semantic_data_exfiltration",
            sensitive_data,
        ),
        (
            "semantic_tool_abuse",
            tool_abuse,
        ),
        (
            "semantic_jailbreak",
            safety_bypass,
        ),
        (
            "semantic_malicious_code",
            malicious_code,
        ),
    ]

    for category, patterns in pattern_groups:

        if _matches_any(text, patterns):

            return {
                "action": "block",
                "risk": 0.95,
                "category": category,
                "reason": (
                    f"Semantic risk detected: {category}"
                ),
                "method": "mock_llm",
            }

    # -------------------------------------------------
    # Default
    # -------------------------------------------------

    return {
        "action": "allow",
        "risk": 0.05,
        "category": "benign",
        "reason": "No semantic risk detected",
        "method": "mock_llm",
    }
