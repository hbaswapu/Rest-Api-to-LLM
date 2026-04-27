#!/usr/bin/env python3
"""
Interactive CLI for the LLM orchestrator.

Prerequisites:
  1. Start the REST API:  python run_api.py
  2. Set ANTHROPIC_API_KEY in your environment or .env file
  3. Run this script:     python run_orchestrator.py
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

# Validate env
if not os.environ.get("ANTHROPIC_API_KEY"):
    raise SystemExit(
        "ERROR: ANTHROPIC_API_KEY is not set.\n"
        "Copy .env.example to .env and fill in your key."
    )

from llm_orchestrator.orchestrator import Orchestrator

BANNER = """
╔══════════════════════════════════════════════════════════╗
║         Banking LLM Orchestrator  (Claude)               ║
║  Type your request in plain English.                     ║
║  Commands: 'reset' to clear history, 'quit' to exit.    ║
╚══════════════════════════════════════════════════════════╝
"""

EXAMPLES = """
Try asking:
  • "Show me all users"
  • "What's the balance on Alice's checking account?"
  • "How many reward points does Bob have?"
  • "List all cards for user u001"
  • "Create a new user named Dave with email dave@example.com"
  • "Block card c003"
"""


def main():
    print(BANNER)
    print(EXAMPLES)

    orch = Orchestrator()
    verbose = os.getenv("VERBOSE", "").lower() in ("1", "true", "yes")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        if user_input.lower() == "reset":
            orch.reset()
            print("Conversation history cleared.\n")
            continue

        reply = orch.chat(user_input, verbose=verbose)
        print(f"\nAssistant: {reply}\n")


if __name__ == "__main__":
    main()
