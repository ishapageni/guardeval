
DANGEROUS_TOOLS = {
    "delete_user",
    "delete_users",
    "drop_database",
    "execute_shell",
    "modify_permissions",
}

SENSITIVE_TOOLS = {
    "read_private_data",
    "read_credentials",
    "export_customer_data",
}


def check_tool_call(
    tool_name: str,
    arguments: dict | None = None
) -> dict:
    """
    Evaluate an agent tool call before execution.
    """

    arguments = arguments or {}

    # Completely dangerous operations
    if tool_name in DANGEROUS_TOOLS:
        return {
            "action": "block",
            "risk": 1.0,
            "category": "dangerous_tool",
            "reason": f"Tool '{tool_name}' requires authorization",
        }

    # Sensitive information access
    if tool_name in SENSITIVE_TOOLS:
        return {
            "action": "review",
            "risk": 0.75,
            "category": "sensitive_tool",
            "reason": f"Tool '{tool_name}' accesses sensitive resources",
        }

    # Otherwise allow
    return {
        "action": "allow",
        "risk": 0.05,
        "category": "safe_tool",
        "reason": "Tool call passed policy checks",
    }
