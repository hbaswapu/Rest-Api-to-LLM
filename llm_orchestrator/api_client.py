"""
Thin HTTP client that wraps the REST API.
All methods return the parsed JSON response (dict or list).
"""
import httpx
import os

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


def _get(path: str, params: dict | None = None) -> dict | list:
    with httpx.Client(base_url=BASE_URL, timeout=10) as client:
        r = client.get(path, params=params)
        r.raise_for_status()
        return r.json()


def _post(path: str, body: dict | None = None, params: dict | None = None) -> dict:
    with httpx.Client(base_url=BASE_URL, timeout=10) as client:
        r = client.post(path, json=body, params=params)
        r.raise_for_status()
        return r.json()


def _patch(path: str, body: dict | None = None) -> dict:
    with httpx.Client(base_url=BASE_URL, timeout=10) as client:
        r = client.patch(path, json=body)
        r.raise_for_status()
        return r.json()


def _put(path: str, body: dict | None = None) -> dict:
    with httpx.Client(base_url=BASE_URL, timeout=10) as client:
        r = client.put(path, json=body)
        r.raise_for_status()
        return r.json()


def _delete(path: str) -> dict:
    with httpx.Client(base_url=BASE_URL, timeout=10) as client:
        r = client.delete(path)
        r.raise_for_status()
        return r.json()


# ── Users ────────────────────────────────────────────────────────────────────

def list_users() -> list:
    return _get("/users/")

def get_user(user_id: str) -> dict:
    return _get(f"/users/{user_id}")

def create_user(name: str, email: str, phone: str | None = None) -> dict:
    return _post("/users/", {"name": name, "email": email, "phone": phone})

def update_user(user_id: str, name: str, email: str, phone: str | None = None) -> dict:
    return _put(f"/users/{user_id}", {"name": name, "email": email, "phone": phone})

def delete_user(user_id: str) -> dict:
    return _delete(f"/users/{user_id}")


# ── Accounts ─────────────────────────────────────────────────────────────────

def list_accounts(user_id: str | None = None) -> list:
    return _get("/accounts/", params={"user_id": user_id} if user_id else None)

def get_account(account_id: str) -> dict:
    return _get(f"/accounts/{account_id}")

def create_account(user_id: str, account_type: str, currency: str = "USD") -> dict:
    return _post("/accounts/", {"user_id": user_id, "account_type": account_type, "currency": currency})

def get_balance(account_id: str) -> dict:
    return _get(f"/accounts/{account_id}/balance")

def freeze_account(account_id: str) -> dict:
    return _patch(f"/accounts/{account_id}/freeze")

def unfreeze_account(account_id: str) -> dict:
    return _patch(f"/accounts/{account_id}/unfreeze")

def close_account(account_id: str) -> dict:
    return _delete(f"/accounts/{account_id}")


# ── Rewards ───────────────────────────────────────────────────────────────────

def get_rewards(user_id: str) -> dict:
    return _get(f"/rewards/{user_id}")

def earn_points(user_id: str, points: int) -> dict:
    return _post(f"/rewards/{user_id}/earn", params={"points": points})

def redeem_points(user_id: str, points: int) -> dict:
    return _post(f"/rewards/{user_id}/redeem", body={"user_id": user_id, "points": points})


# ── Cards ─────────────────────────────────────────────────────────────────────

def list_cards(user_id: str | None = None) -> list:
    return _get("/cards/", params={"user_id": user_id} if user_id else None)

def get_card(card_id: str) -> dict:
    return _get(f"/cards/{card_id}")

def issue_card(user_id: str, account_id: str, card_type: str) -> dict:
    return _post("/cards/", {"user_id": user_id, "account_id": account_id, "card_type": card_type})

def block_card(card_id: str) -> dict:
    return _patch(f"/cards/{card_id}/block")

def unblock_card(card_id: str) -> dict:
    return _patch(f"/cards/{card_id}/unblock")

def cancel_card(card_id: str) -> dict:
    return _delete(f"/cards/{card_id}")
