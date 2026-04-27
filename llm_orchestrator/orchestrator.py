"""
LLM Orchestrator — uses Claude with tool-use to route natural-language
requests to the appropriate REST API endpoints.

Flow:
  User message
    → Claude (decides which tool / API to call)
    → api_client (calls the real REST API)
    → Claude (formats the result into a natural-language reply)
    → User
"""
import json
import os
from typing import Generator

import anthropic
from llm_orchestrator import api_client
from llm_orchestrator.tools import TOOLS

MODEL = "claude-sonnet-4-6"

SYSTEM_PROMPT = """You are a smart banking assistant with access to a set of REST API tools.

When the user asks a question or makes a request, you decide which tool(s) to call,
execute them, and then reply in clear, friendly, natural language.

Guidelines:
- Always confirm destructive operations (delete, close, cancel, block) before acting —
  unless the user has already confirmed.
- When listing resources, summarise the key fields rather than dumping raw JSON.
- If an API call fails, explain the error to the user in plain English.
- Prefer calling the most specific tool first (e.g. get_balance instead of get_account
  when the user only asks about the balance).
- You may chain multiple tool calls in a single turn when it is efficient to do so.
"""


def _dispatch(tool_name: str, tool_input: dict) -> str:
    """Call the correct api_client function and return a JSON string result."""
    fn_map = {
        # Users
        "list_users": lambda i: api_client.list_users(),
        "get_user": lambda i: api_client.get_user(i["user_id"]),
        "create_user": lambda i: api_client.create_user(i["name"], i["email"], i.get("phone")),
        "update_user": lambda i: api_client.update_user(i["user_id"], i["name"], i["email"], i.get("phone")),
        "delete_user": lambda i: api_client.delete_user(i["user_id"]),
        # Accounts
        "list_accounts": lambda i: api_client.list_accounts(i.get("user_id")),
        "get_account": lambda i: api_client.get_account(i["account_id"]),
        "create_account": lambda i: api_client.create_account(i["user_id"], i["account_type"], i.get("currency", "USD")),
        "get_balance": lambda i: api_client.get_balance(i["account_id"]),
        "freeze_account": lambda i: api_client.freeze_account(i["account_id"]),
        "unfreeze_account": lambda i: api_client.unfreeze_account(i["account_id"]),
        "close_account": lambda i: api_client.close_account(i["account_id"]),
        # Rewards
        "get_rewards": lambda i: api_client.get_rewards(i["user_id"]),
        "earn_points": lambda i: api_client.earn_points(i["user_id"], i["points"]),
        "redeem_points": lambda i: api_client.redeem_points(i["user_id"], i["points"]),
        # Cards
        "list_cards": lambda i: api_client.list_cards(i.get("user_id")),
        "get_card": lambda i: api_client.get_card(i["card_id"]),
        "issue_card": lambda i: api_client.issue_card(i["user_id"], i["account_id"], i["card_type"]),
        "block_card": lambda i: api_client.block_card(i["card_id"]),
        "unblock_card": lambda i: api_client.unblock_card(i["card_id"]),
        "cancel_card": lambda i: api_client.cancel_card(i["card_id"]),
    }

    fn = fn_map.get(tool_name)
    if fn is None:
        return json.dumps({"error": f"Unknown tool: {tool_name}"})

    try:
        result = fn(tool_input)
        return json.dumps(result, indent=2)
    except Exception as exc:
        return json.dumps({"error": str(exc)})


class Orchestrator:
    """
    Stateful multi-turn orchestrator.

    Usage:
        orch = Orchestrator()
        reply = orch.chat("What's the balance on account a001?")
        print(reply)
    """

    def __init__(self):
        self._client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        self._history: list[dict] = []

    def chat(self, user_message: str, *, verbose: bool = False) -> str:
        """
        Send a user message, run the agentic tool-use loop, and return
        the final assistant text reply.
        """
        self._history.append({"role": "user", "content": user_message})

        while True:
            response = self._client.messages.create(
                model=MODEL,
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                tools=TOOLS,
                messages=self._history,
            )

            # Append assistant response to history
            self._history.append({"role": "assistant", "content": response.content})

            if response.stop_reason == "end_turn":
                # Extract the final text block
                text_blocks = [b.text for b in response.content if hasattr(b, "text")]
                return "\n".join(text_blocks)

            if response.stop_reason == "tool_use":
                tool_results = []
                for block in response.content:
                    if block.type != "tool_use":
                        continue

                    if verbose:
                        print(f"  [tool] {block.name}({json.dumps(block.input)})")

                    result_str = _dispatch(block.name, block.input)

                    if verbose:
                        print(f"  [result] {result_str[:200]}")

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result_str,
                    })

                # Feed tool results back to Claude
                self._history.append({"role": "user", "content": tool_results})
                continue

            # Unexpected stop reason
            break

        return "(No response)"

    def reset(self):
        """Clear conversation history."""
        self._history = []
