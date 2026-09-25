
import re


BLOCK_PATTERNS = [

    # =================================================
    # PROMPT INJECTION / INSTRUCTION OVERRIDE
    # =================================================

    r"ignore\s+(all\s+)?(previous|prior|earlier)\s+instructions",
    r"forget\s+(all\s+)?(previous|prior|earlier)\s+instructions",
    r"disregard\s+(all\s+)?(previous|prior|earlier)\s+(instructions|rules)",

    r"(assume|treat)\s+.*(instructions|rules).*(invalid|void|ignored)",
    r"(previous|prior|earlier)\s+(instructions|rules).*(invalid|void|ignored)",
    r"(ignore|disregard|override)\s+.*(previous|prior|earlier|existing|current)\s+(instructions|rules)",
    r"(ignore|disregard|override)\s+.*(instructions|rules).*(earlier|previous|prior|existing|current)",

    # Explicit instruction override
    r"(override|replace|supersede)\s+.*(instructions|rules)",
    r"(override|replace|supersede)\s+.*(currently|existing|original)",

    # =================================================
    # SYSTEM / HIDDEN INSTRUCTION EXTRACTION
    # =================================================

    r"(reveal|show|print|display|provide|tell)\s+.*(system|hidden)\s+(prompt|instructions)",
    r"(reveal|show|print|display|provide|tell)\s+.*hidden\s+instructions",

    r"(confidential|secret|protected)\s+.*(initialization|system)\s+(message|prompt|instructions)",

    # =================================================
    # DATA / INFORMATION EXFILTRATION
    # =================================================

    r"(show|give|provide|reveal|send|export|retrieve|obtain)\s+.*(password|credentials|api\s*key|secret|token)",

    r"(show|give|provide|reveal|send|export|retrieve|obtain)\s+.*(private|confidential|sensitive)\s+.*(information|data|records)",

    r"(show|give|provide|reveal|send|export|retrieve|obtain)\s+.*(customer|client|user)\s+(information|data|records)",

    # Requests phrased as "I need ..."
    r"(i\s+need|i\s+want|please\s+provide|please\s+send)\s+.*(private|confidential|sensitive)\s+.*(information|data|records)",

    r"(i\s+need|i\s+want|please\s+provide|please\s+send)\s+.*(customer|client|user)\s+(information|data|records)",

    # =================================================
    # DESTRUCTIVE TOOL ACTIONS
    # =================================================

    r"(delete|remove|drop|erase|destroy)\s+.*(all|every)\s+.*users?",
    r"(delete|remove|drop|erase|destroy)\s+.*(all|every)\s+.*user\s+accounts?",

    # Destructive action + production/database/system
    r"(delete|remove|drop|erase|destroy)\s+.*(production|database|system)",

    # =================================================
    # JAILBREAK / SAFETY BYPASS
    # =================================================

    r"no\s+safety\s+restrictions",
    r"(ignore|disable|bypass|circumvent)\s+.*safety",
    r"(disable|remove|turn\s+off)\s+.*(safety|security)\s+(controls|mechanisms|filters|restrictions)",

]


def check_input(prompt: str) -> dict:
    normalized = prompt.lower().strip()

    for pattern in BLOCK_PATTERNS:
        if re.search(pattern, normalized):
            return {
                "action": "block",
                "risk": 1.0,
                "reason": "Matched unsafe input pattern",
            }

    return {
        "action": "allow",
        "risk": 0.0,
        "reason": "No unsafe pattern detected",
    }
