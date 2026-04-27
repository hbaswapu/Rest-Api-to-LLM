from fastapi import APIRouter, HTTPException
from rest_api.models import Reward, RewardRedeem, MessageResponse
from rest_api import data

router = APIRouter(prefix="/rewards", tags=["Rewards"])

TIER_THRESHOLDS = [
    (10_000, "platinum"),
    (5_000, "gold"),
    (2_500, "silver"),
    (0, "bronze"),
]

def _compute_tier(points: int) -> str:
    for threshold, tier in TIER_THRESHOLDS:
        if points >= threshold:
            return tier
    return "bronze"


@router.get("/{user_id}", response_model=Reward)
def get_rewards(user_id: str):
    """Return rewards info for a user."""
    if user_id not in data.users:
        raise HTTPException(status_code=404, detail=f"User '{user_id}' not found")
    reward = data.rewards.get(user_id)
    if not reward:
        # Auto-create rewards record on first access
        rid = data.next_id("reward")
        reward = {
            "id": rid,
            "user_id": user_id,
            "points_balance": 0,
            "tier": "bronze",
            "last_earned_at": None,
        }
        data.rewards[user_id] = reward
    return reward


@router.post("/{user_id}/earn")
def earn_points(user_id: str, points: int):
    """Add reward points to a user's balance."""
    if user_id not in data.users:
        raise HTTPException(status_code=404, detail=f"User '{user_id}' not found")
    if points <= 0:
        raise HTTPException(status_code=400, detail="Points must be a positive integer")
    from datetime import datetime, timezone
    reward = data.rewards.setdefault(user_id, {
        "id": data.next_id("reward"),
        "user_id": user_id,
        "points_balance": 0,
        "tier": "bronze",
        "last_earned_at": None,
    })
    reward["points_balance"] += points
    reward["tier"] = _compute_tier(reward["points_balance"])
    reward["last_earned_at"] = datetime.now(timezone.utc).isoformat()
    return reward


@router.post("/{user_id}/redeem")
def redeem_points(user_id: str, body: RewardRedeem):
    """Redeem reward points from a user's balance."""
    if user_id not in data.users:
        raise HTTPException(status_code=404, detail=f"User '{user_id}' not found")
    reward = data.rewards.get(user_id)
    if not reward:
        raise HTTPException(status_code=404, detail="No rewards record found")
    if body.points <= 0:
        raise HTTPException(status_code=400, detail="Points must be a positive integer")
    if reward["points_balance"] < body.points:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient points. Balance: {reward['points_balance']}, requested: {body.points}",
        )
    reward["points_balance"] -= body.points
    reward["tier"] = _compute_tier(reward["points_balance"])
    return reward
