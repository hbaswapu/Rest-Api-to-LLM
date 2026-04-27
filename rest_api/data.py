"""
In-memory mock data store.
All collections are plain dicts keyed by resource id.
"""
from datetime import datetime, timezone

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# Seed data ───────────────────────────────────────────────────────────────────

users: dict = {
    "u001": {
        "id": "u001",
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "phone": "+1-555-0101",
        "created_at": "2024-01-15T10:00:00+00:00",
    },
    "u002": {
        "id": "u002",
        "name": "Bob Smith",
        "email": "bob@example.com",
        "phone": "+1-555-0102",
        "created_at": "2024-02-20T14:30:00+00:00",
    },
    "u003": {
        "id": "u003",
        "name": "Carol White",
        "email": "carol@example.com",
        "phone": None,
        "created_at": "2024-03-05T09:15:00+00:00",
    },
}

accounts: dict = {
    "a001": {
        "id": "a001",
        "user_id": "u001",
        "account_type": "checking",
        "currency": "USD",
        "balance": 4250.75,
        "status": "active",
        "created_at": "2024-01-16T08:00:00+00:00",
    },
    "a002": {
        "id": "a002",
        "user_id": "u001",
        "account_type": "savings",
        "currency": "USD",
        "balance": 12000.00,
        "status": "active",
        "created_at": "2024-01-16T08:05:00+00:00",
    },
    "a003": {
        "id": "a003",
        "user_id": "u002",
        "account_type": "checking",
        "currency": "USD",
        "balance": 870.20,
        "status": "active",
        "created_at": "2024-02-21T09:00:00+00:00",
    },
}

rewards: dict = {
    "u001": {
        "id": "r001",
        "user_id": "u001",
        "points_balance": 8500,
        "tier": "gold",
        "last_earned_at": "2024-10-01T12:00:00+00:00",
    },
    "u002": {
        "id": "r002",
        "user_id": "u002",
        "points_balance": 1200,
        "tier": "bronze",
        "last_earned_at": "2024-09-15T16:00:00+00:00",
    },
    "u003": {
        "id": "r003",
        "user_id": "u003",
        "points_balance": 3400,
        "tier": "silver",
        "last_earned_at": "2024-10-10T08:00:00+00:00",
    },
}

cards: dict = {
    "c001": {
        "id": "c001",
        "user_id": "u001",
        "account_id": "a001",
        "card_type": "debit",
        "last_four": "4321",
        "status": "active",
        "expires": "2027-01",
        "credit_limit": None,
    },
    "c002": {
        "id": "c002",
        "user_id": "u001",
        "account_id": "a001",
        "card_type": "credit",
        "last_four": "8765",
        "status": "active",
        "expires": "2026-06",
        "credit_limit": 5000.00,
    },
    "c003": {
        "id": "c003",
        "user_id": "u002",
        "account_id": "a003",
        "card_type": "debit",
        "last_four": "1122",
        "status": "blocked",
        "expires": "2025-12",
        "credit_limit": None,
    },
}

# Counters for auto-generated IDs
_counters: dict = {"user": 4, "account": 4, "reward": 4, "card": 4}

def next_id(kind: str) -> str:
    prefix = {"user": "u", "account": "a", "reward": "r", "card": "c"}[kind]
    n = _counters[kind]
    _counters[kind] += 1
    return f"{prefix}{n:03d}"
