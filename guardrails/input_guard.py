
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
       # BROADER PROMPT INJECTION
    r"(ignore|disregard|replace|override|supersede)\s+.*(previous|prior|earlier|existing|current)\s+(instructions|rules|guidance|constraints|policy)",
    r"(previous|prior|earlier)\s+(instructions|rules|guidance|policy).*(no longer|no longer applies|revoked|obsolete)",
    r"(change|replace|override|supersede)\s+.*(priority|instruction|rules|policy)",
    r"(follow|use)\s+(only|just)\s+.*(this message|this directive|these instructions)",

    # BROADER DATA EXFILTRATION
    r"(reveal|show|provide|return|extract|display|expose|print|list|give).*(hidden|internal|private|confidential|protected|secret|sensitive).*(information|data|records|configuration|instructions|credentials)",
    r"(reveal|show|provide|return|extract|display|expose|print|list|give).*(system|internal|hidden).*(prompt|instructions|configuration)",
    r"(provide|return|show|list|give).*(password|credential|token|api\s*key|secret)",
    r"(private|confidential|sensitive|protected).*(customer|client|user).*(information|data|records)",
    r"(authentication|credential|token|api\s*key).*(available|accessible|used|stored)",

    # BROADER DESTRUCTIVE / PRIVILEGED TOOL ACTIONS
    r"(delete|remove|erase|destroy|drop|disable|wipe).*(database|table|account|user|file|directory|application|system|data)",
    r"(execute|invoke|call|use|run).*(deletion|destructive|privileged|administrative|admin).*(operation|command|tool|action)",
    r"(disable|remove|revoke).*(all|every|user|account|security|authorization)",
    r"(grant|give|assign).*(admin|administrator|privileged).*(access|permission|privileges)",
    r"(bypass|skip|circumvent).*(authorization|authentication|security|access\s*control)",

    # BROADER JAILBREAK / SAFETY BYPASS
    r"(unrestricted|unconstrained).*(assistant|model|mode|simulation)",
    r"(no|without|zero)\s+(safety|security)\s+(constraints|restrictions|controls|limits)",
    r"(ignore|disable|remove|turn\s+off|bypass).*(safety|security).*(rules|restrictions|controls|safeguards)",
    r"(developer|debug|admin|administrator)\s+mode.*(restrictions|safety|security|safeguards)",
    r"(safety|security|policy).*(disabled|removed|turned\s+off|bypassed)",
    r"(pretend|act|roleplay|simulate|assume).*(no\s+safety|unrestricted|without\s+restrictions|safeguards\s+disabled)",
    r"(restrictions|safeguards|security\s+checks|policy\s+layer).*(removed|disabled|bypassed|turned\s+off)",
       # REMAINING PROMPT INJECTION PATTERNS
    r"(fresh|new)\s+instruction\s+hierarchy.*(disregard|ignore|replace|override)",
    r"(previous|existing|earlier)\s+(safety\s+)?(guidance|instructions|rules).*(revoked|replaced|superseded|no longer)",
    r"(message|directive).*(authoritative|highest|priority).*(instruction|rule|policy)",
    r"(suspend|ignore|disregard).*(existing|current|previous).*(constraints|instructions|rules|policy)",
    r"(instruction\s+hierarchy|instruction\s+priority).*(ignore|disregard|override|bypass)",
    
    # REMAINING DATA EXFILTRATION PATTERNS
    r"what\s+(confidential|private|sensitive|protected).*(available|accessible|stored).*(context|environment|system)",
    r"(show|provide|return|display|expose).*(protected|restricted).*(records|information|data|variables)",
    r"(information|records|data).*(restricted|protected|private).*(ordinary\s+users|users).*(cannot|can't|not\s+allowed)",
    
    # REMAINING TOOL ABUSE PATTERNS
    r"(payment|billing|refund)\s+tool.*(unauthorized|unapproved)",
    r"(database|db)\s+tool.*(modify|change|update|alter).*(every|all|customer|user|record)",
    r"(credential|credential-management|authentication)\s+tool.*(rotate|change|modify|reset).*(without|no)\s+(approval|authorization)",
    r"(filesystem|file-access|file\s+access)\s+tool.*(private|secret|protected|sensitive)",
    r"(network|networking)\s+tool.*(unapproved|unauthorized|external)",
    r"(account|user-management|user)\s+tool.*(another\s+user|other\s+user).*(authentication|security|settings)",
    r"(file-access|filesystem)\s+tool.*(protected|system).*(directory|path)",
    
    # REMAINING JAILBREAK PATTERNS
    r"(roleplay|role-play|pretend|act\s+as).*(system|assistant|administrator|admin).*(ignore|bypass|disregard).*(security|safety|policy|restrictions)",
    r"(imagine|suppose|assume).*(safety|security)\s+(rules|restrictions).*(do\s+not|don't)\s+exist",
    r"(fictional|hypothetical).*(assistant|administrator|admin|system).*(safeguard|restriction|security|policy).*(disabled|removed|bypassed)",
    r"(unrestricted)\s+(administrator|admin|assistant|model)",
    r"(fictional\s+persona|persona).*(priority|precedence).*(system|security|safeguard|policy)",
    r"(simulate|pretend|act\s+as).*(version|copy).*(yourself|assistant|model).*(without|not\s+follow).*(restriction|rule|policy)",
   r"(do not|don't)\s+use\s+(the\s+)?instructions?\s+(established|given|provided)\s+(earlier|before)",
r"(ignore|disregard)\s+(the\s+)?instruction\s+hierarchy",

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
