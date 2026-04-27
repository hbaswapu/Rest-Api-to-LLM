from fastapi import APIRouter, HTTPException, Query
from rest_api.models import Account, AccountCreate, MessageResponse
from rest_api import data

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.get("/", response_model=list[Account])
def list_accounts(user_id: str | None = Query(default=None)):
    """List all accounts, optionally filtered by user_id."""
    accounts = list(data.accounts.values())
    if user_id:
        accounts = [a for a in accounts if a["user_id"] == user_id]
    return accounts


@router.get("/{account_id}", response_model=Account)
def get_account(account_id: str):
    """Return a single account by ID."""
    acct = data.accounts.get(account_id)
    if not acct:
        raise HTTPException(status_code=404, detail=f"Account '{account_id}' not found")
    return acct


@router.post("/", response_model=Account, status_code=201)
def create_account(body: AccountCreate):
    """Open a new account for a user."""
    if body.user_id not in data.users:
        raise HTTPException(status_code=404, detail=f"User '{body.user_id}' not found")
    from datetime import datetime, timezone
    aid = data.next_id("account")
    account = {
        "id": aid,
        "user_id": body.user_id,
        "account_type": body.account_type,
        "currency": body.currency,
        "balance": 0.0,
        "status": "active",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    data.accounts[aid] = account
    return account


@router.patch("/{account_id}/freeze", response_model=Account)
def freeze_account(account_id: str):
    """Freeze an account."""
    acct = data.accounts.get(account_id)
    if not acct:
        raise HTTPException(status_code=404, detail=f"Account '{account_id}' not found")
    acct["status"] = "frozen"
    return acct


@router.patch("/{account_id}/unfreeze", response_model=Account)
def unfreeze_account(account_id: str):
    """Unfreeze an account."""
    acct = data.accounts.get(account_id)
    if not acct:
        raise HTTPException(status_code=404, detail=f"Account '{account_id}' not found")
    acct["status"] = "active"
    return acct


@router.get("/{account_id}/balance")
def get_balance(account_id: str):
    """Return just the balance for an account."""
    acct = data.accounts.get(account_id)
    if not acct:
        raise HTTPException(status_code=404, detail=f"Account '{account_id}' not found")
    return {"account_id": account_id, "balance": acct["balance"], "currency": acct["currency"]}


@router.delete("/{account_id}", response_model=MessageResponse)
def close_account(account_id: str):
    """Close (delete) an account."""
    if account_id not in data.accounts:
        raise HTTPException(status_code=404, detail=f"Account '{account_id}' not found")
    del data.accounts[account_id]
    return {"message": f"Account '{account_id}' closed successfully"}
