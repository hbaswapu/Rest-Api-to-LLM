from fastapi import APIRouter, HTTPException, Query
from rest_api.models import Card, CardCreate, MessageResponse
from rest_api import data

router = APIRouter(prefix="/cards", tags=["Cards"])


@router.get("/", response_model=list[Card])
def list_cards(user_id: str | None = Query(default=None)):
    """List all cards, optionally filtered by user_id."""
    cards = list(data.cards.values())
    if user_id:
        cards = [c for c in cards if c["user_id"] == user_id]
    return cards


@router.get("/{card_id}", response_model=Card)
def get_card(card_id: str):
    """Return a single card by ID."""
    card = data.cards.get(card_id)
    if not card:
        raise HTTPException(status_code=404, detail=f"Card '{card_id}' not found")
    return card


@router.post("/", response_model=Card, status_code=201)
def issue_card(body: CardCreate):
    """Issue a new card for a user/account."""
    if body.user_id not in data.users:
        raise HTTPException(status_code=404, detail=f"User '{body.user_id}' not found")
    if body.account_id not in data.accounts:
        raise HTTPException(status_code=404, detail=f"Account '{body.account_id}' not found")
    import random, string
    cid = data.next_id("card")
    last_four = "".join(random.choices(string.digits, k=4))
    card = {
        "id": cid,
        "user_id": body.user_id,
        "account_id": body.account_id,
        "card_type": body.card_type,
        "last_four": last_four,
        "status": "active",
        "expires": "2028-01",
        "credit_limit": 3000.00 if body.card_type == "credit" else None,
    }
    data.cards[cid] = card
    return card


@router.patch("/{card_id}/block", response_model=Card)
def block_card(card_id: str):
    """Block a card."""
    card = data.cards.get(card_id)
    if not card:
        raise HTTPException(status_code=404, detail=f"Card '{card_id}' not found")
    card["status"] = "blocked"
    return card


@router.patch("/{card_id}/unblock", response_model=Card)
def unblock_card(card_id: str):
    """Unblock a card."""
    card = data.cards.get(card_id)
    if not card:
        raise HTTPException(status_code=404, detail=f"Card '{card_id}' not found")
    card["status"] = "active"
    return card


@router.delete("/{card_id}", response_model=MessageResponse)
def cancel_card(card_id: str):
    """Cancel (delete) a card."""
    if card_id not in data.cards:
        raise HTTPException(status_code=404, detail=f"Card '{card_id}' not found")
    del data.cards[card_id]
    return {"message": f"Card '{card_id}' cancelled successfully"}
