# Rest-Api-to-LLM

> **Converting a REST API into LLM model orchestration** — users talk in plain English; Claude decides which API to call.

```
User (natural language)
        │
        ▼
  LLM Orchestrator  (Claude + tool-use)
        │
        ├──▶  /users       ──▶  Users API
        ├──▶  /accounts    ──▶  Accounts API
        ├──▶  /rewards     ──▶  Rewards API
        └──▶  /cards       ──▶  Cards API
```

---

## What this project does

| Layer | Description |
|---|---|
| **REST API** (`rest_api/`) | FastAPI app with four resource groups: Users, Accounts, Rewards, Cards. Fully CRUD, in-memory data store, OpenAPI docs at `/docs`. |
| **LLM Orchestrator** (`llm_orchestrator/`) | Claude-powered agent that receives natural-language requests, selects the right REST endpoint via tool-use, calls it through `api_client.py`, and returns a human-friendly answer. |

---

## Project structure

```
.
├── rest_api/
│   ├── app.py          # FastAPI application
│   ├── models.py       # Pydantic request/response models
│   ├── data.py         # In-memory data + seed records
│   └── routes/
│       ├── users.py    # GET/POST/PUT/DELETE /users
│       ├── accounts.py # GET/POST/PATCH/DELETE /accounts
│       ├── rewards.py  # GET /rewards, POST /earn, /redeem
│       └── cards.py    # GET/POST/PATCH/DELETE /cards
│
├── llm_orchestrator/
│   ├── tools.py        # Claude tool definitions (1 per API action)
│   ├── api_client.py   # HTTP wrapper around the REST API
│   └── orchestrator.py # Agentic loop: Claude ↔ tool dispatch
│
├── run_api.py          # Start the REST API server
├── run_orchestrator.py # Start the interactive CLI chat
├── requirements.txt
└── .env.example
```

---

## Quick start

### 1. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 3. Start the REST API

```bash
python run_api.py
# → http://localhost:8000
# → Swagger UI: http://localhost:8000/docs
```

### 4. Start the LLM orchestrator (in a second terminal)

```bash
python run_orchestrator.py
```

---

## Example interactions

```
You: Show me all users
Assistant: There are 3 users: Alice Johnson (u001), Bob Smith (u002), Carol White (u003).

You: What is the balance on Alice's checking account?
Assistant: Alice's checking account (a001) has a balance of $4,250.75 USD.

You: How many reward points does Bob have?
Assistant: Bob currently has 1,200 reward points and is in the Bronze tier.

You: Block card c003
Assistant: Card c003 (ending in 1122) has been blocked successfully.

You: Create a new savings account for user u002
Assistant: Done! I've opened a new savings account (a004) for Bob Smith in USD with a starting balance of $0.00.
```

---

## REST API endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/users/` | List all users |
| POST | `/users/` | Create user |
| GET | `/users/{id}` | Get user |
| PUT | `/users/{id}` | Update user |
| DELETE | `/users/{id}` | Delete user |
| GET | `/accounts/` | List accounts (filter: `?user_id=`) |
| POST | `/accounts/` | Open account |
| GET | `/accounts/{id}/balance` | Get balance |
| PATCH | `/accounts/{id}/freeze` | Freeze account |
| PATCH | `/accounts/{id}/unfreeze` | Unfreeze account |
| DELETE | `/accounts/{id}` | Close account |
| GET | `/rewards/{user_id}` | Get rewards & tier |
| POST | `/rewards/{user_id}/earn` | Add points |
| POST | `/rewards/{user_id}/redeem` | Redeem points |
| GET | `/cards/` | List cards (filter: `?user_id=`) |
| POST | `/cards/` | Issue card |
| PATCH | `/cards/{id}/block` | Block card |
| PATCH | `/cards/{id}/unblock` | Unblock card |
| DELETE | `/cards/{id}` | Cancel card |

---

## How the orchestration works

1. **User sends a natural-language message** to the CLI.
2. **Claude receives it** along with the full list of tool definitions (one per API action).
3. **Claude chooses which tool(s) to call** — it may chain multiple calls in one turn (e.g. look up a user then list their accounts).
4. **`_dispatch()`** translates the tool call into a real HTTP request via `api_client.py`.
5. **Tool results are fed back to Claude**, which then writes a friendly reply to the user.
6. **Conversation history is maintained** across turns for multi-step requests.
