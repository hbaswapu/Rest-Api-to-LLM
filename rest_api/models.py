from pydantic import BaseModel
from typing import Optional
from datetime import date


# ── Users ────────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None


class User(UserCreate):
    id: str
    created_at: str


# ── Accounts ─────────────────────────────────────────────────────────────────

class AccountCreate(BaseModel):
    user_id: str
    account_type: str   # "checking" | "savings"
    currency: str = "USD"


class Account(AccountCreate):
    id: str
    balance: float
    status: str         # "active" | "frozen" | "closed"
    created_at: str


# ── Rewards ───────────────────────────────────────────────────────────────────

class RewardRedeem(BaseModel):
    user_id: str
    points: int


class Reward(BaseModel):
    id: str
    user_id: str
    points_balance: int
    tier: str           # "bronze" | "silver" | "gold" | "platinum"
    last_earned_at: Optional[str] = None


# ── Cards ─────────────────────────────────────────────────────────────────────

class CardCreate(BaseModel):
    user_id: str
    account_id: str
    card_type: str      # "debit" | "credit"


class Card(CardCreate):
    id: str
    last_four: str
    status: str         # "active" | "blocked" | "expired"
    expires: str
    credit_limit: Optional[float] = None


# ── Generic responses ─────────────────────────────────────────────────────────

class MessageResponse(BaseModel):
    message: str
