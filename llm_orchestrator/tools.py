"""
Claude tool definitions.
Each tool maps 1-to-1 with an api_client function.
"""

TOOLS: list[dict] = [
    # ── Users ────────────────────────────────────────────────────────────────
    {
        "name": "list_users",
        "description": "List all users in the system.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "get_user",
        "description": "Get details of a specific user by their user ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "The user's ID (e.g. 'u001')"},
            },
            "required": ["user_id"],
        },
    },
    {
        "name": "create_user",
        "description": "Create a new user account.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Full name"},
                "email": {"type": "string", "description": "Email address"},
                "phone": {"type": "string", "description": "Phone number (optional)"},
            },
            "required": ["name", "email"],
        },
    },
    {
        "name": "update_user",
        "description": "Update an existing user's information.",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string"},
                "name": {"type": "string"},
                "email": {"type": "string"},
                "phone": {"type": "string"},
            },
            "required": ["user_id", "name", "email"],
        },
    },
    {
        "name": "delete_user",
        "description": "Delete a user from the system.",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string"},
            },
            "required": ["user_id"],
        },
    },

    # ── Accounts ─────────────────────────────────────────────────────────────
    {
        "name": "list_accounts",
        "description": "List all bank accounts. Optionally filter by user_id.",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "Filter by this user ID (optional)"},
            },
            "required": [],
        },
    },
    {
        "name": "get_account",
        "description": "Get details of a specific account by account ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "account_id": {"type": "string"},
            },
            "required": ["account_id"],
        },
    },
    {
        "name": "create_account",
        "description": "Open a new bank account (checking or savings) for a user.",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string"},
                "account_type": {
                    "type": "string",
                    "enum": ["checking", "savings"],
                    "description": "Type of account to open",
                },
                "currency": {
                    "type": "string",
                    "default": "USD",
                    "description": "Currency code (default USD)",
                },
            },
            "required": ["user_id", "account_type"],
        },
    },
    {
        "name": "get_balance",
        "description": "Get the current balance of a specific account.",
        "input_schema": {
            "type": "object",
            "properties": {
                "account_id": {"type": "string"},
            },
            "required": ["account_id"],
        },
    },
    {
        "name": "freeze_account",
        "description": "Freeze a bank account to prevent transactions.",
        "input_schema": {
            "type": "object",
            "properties": {
                "account_id": {"type": "string"},
            },
            "required": ["account_id"],
        },
    },
    {
        "name": "unfreeze_account",
        "description": "Unfreeze a previously frozen bank account.",
        "input_schema": {
            "type": "object",
            "properties": {
                "account_id": {"type": "string"},
            },
            "required": ["account_id"],
        },
    },
    {
        "name": "close_account",
        "description": "Close (permanently delete) a bank account.",
        "input_schema": {
            "type": "object",
            "properties": {
                "account_id": {"type": "string"},
            },
            "required": ["account_id"],
        },
    },

    # ── Rewards ───────────────────────────────────────────────────────────────
    {
        "name": "get_rewards",
        "description": "Get rewards points balance and tier for a user.",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string"},
            },
            "required": ["user_id"],
        },
    },
    {
        "name": "earn_points",
        "description": "Add reward points to a user's rewards balance.",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string"},
                "points": {"type": "integer", "description": "Number of points to add (positive)"},
            },
            "required": ["user_id", "points"],
        },
    },
    {
        "name": "redeem_points",
        "description": "Redeem reward points from a user's balance.",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string"},
                "points": {"type": "integer", "description": "Number of points to redeem"},
            },
            "required": ["user_id", "points"],
        },
    },

    # ── Cards ─────────────────────────────────────────────────────────────────
    {
        "name": "list_cards",
        "description": "List all cards. Optionally filter by user_id.",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "Filter by this user ID (optional)"},
            },
            "required": [],
        },
    },
    {
        "name": "get_card",
        "description": "Get details of a specific card by card ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "card_id": {"type": "string"},
            },
            "required": ["card_id"],
        },
    },
    {
        "name": "issue_card",
        "description": "Issue a new debit or credit card to a user, linked to one of their accounts.",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string"},
                "account_id": {"type": "string"},
                "card_type": {
                    "type": "string",
                    "enum": ["debit", "credit"],
                },
            },
            "required": ["user_id", "account_id", "card_type"],
        },
    },
    {
        "name": "block_card",
        "description": "Block a card to prevent it from being used.",
        "input_schema": {
            "type": "object",
            "properties": {
                "card_id": {"type": "string"},
            },
            "required": ["card_id"],
        },
    },
    {
        "name": "unblock_card",
        "description": "Unblock a previously blocked card.",
        "input_schema": {
            "type": "object",
            "properties": {
                "card_id": {"type": "string"},
            },
            "required": ["card_id"],
        },
    },
    {
        "name": "cancel_card",
        "description": "Cancel (permanently delete) a card.",
        "input_schema": {
            "type": "object",
            "properties": {
                "card_id": {"type": "string"},
            },
            "required": ["card_id"],
        },
    },
]
