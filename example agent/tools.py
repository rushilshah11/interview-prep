tools = [
    {
        "type": "function",
        "function": {
            "name": "get_balance",
            "description": "Get the current USDC balance for the specified wallet.",
            "parameters": {
                "type": "object",
                "properties": {
                    "wallet_id": {
                        "type": "string",
                        "description": "Wallet identifier. Case-insensitive; for example, 'bob' refers to 'Bob'.",
                    },
                },
                "required": ["wallet_id"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "send_payment",
            "description": (
                "Send USDC from one wallet to another. This tool transfers funds. "
                "Invoke it only when the user gives an explicit, unambiguous command "
                "to send a payment, such as 'Send 10 USDC from Alice to Bob.' "
                "Do not invoke it in response to a question, hypothetical, or discussion "
                "about sending a payment (for example, 'Can you send 10 USDC to Bob?'). "
                "If the user is asking whether or how to send a payment, answer without "
                "transferring funds. If required details are missing or ambiguous, ask "
                "for clarification instead of invoking the tool."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "from_id": {
                        "type": "string",
                        "description": "Identifier of the sender's wallet.",
                    },
                    "to_id": {
                        "type": "string",
                        "description": "Identifier of the recipient's wallet.",
                    },
                    "amount_usdc": {
                        "type": "string",
                        "description": "Positive USDC amount as a decimal string, for example '10.25'.",
                    },
                },
                "required": ["from_id", "to_id", "amount_usdc"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_transactions",
            "description": "List the transactions associated with the specified wallet.",
            "parameters": {
                "type": "object",
                "properties": {
                    "wallet_id": {
                        "type": "string",
                        "description": "Wallet identifier. Case-insensitive; for example, 'bob' refers to 'Bob'.",
                    },
                },
                "required": ["wallet_id"],
                "additionalProperties": False,
            },
        },
    },
]
