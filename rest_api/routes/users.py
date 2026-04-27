from fastapi import APIRouter, HTTPException
from rest_api.models import User, UserCreate, MessageResponse
from rest_api import data

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[User])
def list_users():
    """Return all users."""
    return list(data.users.values())


@router.get("/{user_id}", response_model=User)
def get_user(user_id: str):
    """Return a single user by ID."""
    user = data.users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User '{user_id}' not found")
    return user


@router.post("/", response_model=User, status_code=201)
def create_user(body: UserCreate):
    """Create a new user."""
    uid = data.next_id("user")
    from datetime import datetime, timezone
    user = {
        "id": uid,
        "name": body.name,
        "email": body.email,
        "phone": body.phone,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    data.users[uid] = user
    return user


@router.put("/{user_id}", response_model=User)
def update_user(user_id: str, body: UserCreate):
    """Update an existing user."""
    if user_id not in data.users:
        raise HTTPException(status_code=404, detail=f"User '{user_id}' not found")
    data.users[user_id].update(
        name=body.name, email=body.email, phone=body.phone
    )
    return data.users[user_id]


@router.delete("/{user_id}", response_model=MessageResponse)
def delete_user(user_id: str):
    """Delete a user."""
    if user_id not in data.users:
        raise HTTPException(status_code=404, detail=f"User '{user_id}' not found")
    del data.users[user_id]
    return {"message": f"User '{user_id}' deleted successfully"}
