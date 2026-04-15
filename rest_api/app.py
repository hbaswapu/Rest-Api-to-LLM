from fastapi import FastAPI
from rest_api.routes import users, accounts, rewards, cards

app = FastAPI(
    title="Banking REST API",
    description=(
        "A sample banking REST API with Users, Accounts, Rewards, and Cards endpoints. "
        "This API is consumed by the LLM orchestration layer to fulfill natural-language requests."
    ),
    version="1.0.0",
)

app.include_router(users.router)
app.include_router(accounts.router)
app.include_router(rewards.router)
app.include_router(cards.router)


@app.get("/", tags=["Health"])
def health():
    return {"status": "ok", "service": "Banking REST API"}
