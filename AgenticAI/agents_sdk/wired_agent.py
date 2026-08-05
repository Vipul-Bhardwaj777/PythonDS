"""
Simple wiring demo: Agents SDK + system prompt + RAG + mem0 (+ RQ hook)

What each piece does:
  instructions / SYSTEM_PROMPT  -> agent personality + rules (like old system messages)
  SQLiteSession                 -> short-term chat memory (this conversation)
  retrieve_docs tool            -> RAG over your Qdrant collection (from rag/)
  mem0 search/add               -> long-term user facts (from mem0_memory.py/mem_chat.py)
  run_agent_job                 -> same turn logic RQ can enqueue (optional)

Prereqs (same as your earlier projects):
  - Qdrant up, collection learning_rag indexed (rag/index.py)
  - OPENAI_API_KEY
  - mem0's Qdrant (often same docker as mem0_memory.py)

Run from AgenticAI (recommended):
  python -m agents_sdk.wired_agent

Or from this folder:
  python .\\wired_agent.py
"""

from __future__ import annotations

import asyncio
import importlib.util
import json
import sys
from pathlib import Path

from agents import Agent, Runner, SQLiteSession, function_tool
from dotenv import load_dotenv

load_dotenv()

# Make AgenticAI importable when you run this file from agents_sdk/
AGENTIC_ROOT = Path(__file__).resolve().parents[1]
if str(AGENTIC_ROOT) not in sys.path:
    sys.path.insert(0, str(AGENTIC_ROOT))

# --- reuse your RAG vector store (rag/chat.py) ---
from rag.chat import vector_store  # noqa: E402

# --- reuse your mem0 client (folder is named mem0_memory.py, so load by path) ---
_mem_path = AGENTIC_ROOT / "mem0_memory.py" / "mem_chat.py"
_spec = importlib.util.spec_from_file_location("mem_chat_reuse", _mem_path)
assert _spec and _spec.loader
_mem_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mem_mod)
mem_client = _mem_mod.mem_client

USER_ID = "vipulbhardwaj"


# =============================================================================
# 1) SYSTEM PROMPT  ==  Agent(instructions=...)
# =============================================================================
SYSTEM_PROMPT = """
You are a helpful assistant named Billy.

Rules:
- For questions about indexed PDF/documents, call retrieve_docs.
- Use known user facts from the message context when relevant.
- If docs don't contain the answer, say you don't know from the documents.
- Keep answers concise.
"""


# =============================================================================
# 2) RAG as a TOOL (agent decides when to retrieve)
# =============================================================================
@function_tool
def retrieve_docs(query: str) -> str:
    """Search indexed documents (Qdrant learning_rag) for relevant context."""
    hits = vector_store.similarity_search(query)
    if not hits:
        return "No relevant documents found."

    parts = []
    for doc in hits:
        page = doc.metadata.get("page_label", "?")
        source = doc.metadata.get("source", "?")
        parts.append(
            f"Page content: {doc.page_content}\nPage number: {page}\nFile: {source}"
        )
    return "\n\n---\n\n".join(parts)


agent = Agent(
    name="wired_billy",
    model="gpt-4.1-mini",
    instructions=SYSTEM_PROMPT,
    tools=[retrieve_docs],
)


# =============================================================================
# 3) One turn: mem0 (long-term) + session (short-term) + agent
# =============================================================================
async def handle_turn(
    user_query: str,
    session: SQLiteSession,
    user_id: str = USER_ID,
) -> str:
    # A) Long-term memory IN (same idea as mem_chat.py search → system context)
    mem_result = mem_client.search(query=user_query, filters={"user_id": user_id})
    memories = [
        f"Id: {m['id']}\nMemory: {m['memory']}" for m in mem_result.get("results", [])
    ]
    memory_block = json.dumps(memories, indent=2) if memories else "[]"

    # Give the model memories for THIS turn (session still holds chat history)
    grounded_input = (
        f"Known long-term facts about the user:\n{memory_block}\n\n"
        f"User message: {user_query}"
    )

    result = await Runner.run(agent, grounded_input, session=session)
    answer = result.final_output

    # B) Long-term memory OUT (same idea as mem_chat.py add after reply)
    mem_client.add(
        user_id=user_id,
        messages=[
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": str(answer)},
        ],
    )
    return str(answer)


# =============================================================================
# 4) RQ hook — worker would call this (optional; needs Redis + worker)
# =============================================================================
def run_agent_job(user_query: str, session_id: str = "wired_chat") -> str:
    """Sync wrapper so RQ can enqueue the same logic.

    Example (when Valkey/Redis + worker are up):
      from rag_queue.client.rq_client import r_queue
      job = r_queue.enqueue(run_agent_job, "What is on page 3?", "user_123")
    """
    session = SQLiteSession(session_id)
    return asyncio.run(handle_turn(user_query, session=session))


def enqueue_example(query: str) -> str | None:
    """Optional: try enqueue; returns job id or None if Redis isn't running."""
    try:
        from rag_queue.client.rq_client import r_queue

        job = r_queue.enqueue(run_agent_job, query, "wired_rq_chat")
        return job.id
    except Exception as e:
        print(f"(RQ skipped — start Redis/Valkey + worker to use queues: {e})")
        return None


# =============================================================================
# CLI — learn without queues first
# =============================================================================
async def main() -> None:
    session = SQLiteSession("wired_chat")

    while True:
        user_input = input("👉 ").strip()
        if not user_input or user_input.lower() == "q":
            break

        answer = await handle_turn(user_input, session=session)
        print(answer)
        print()


if __name__ == "__main__":
    asyncio.run(main())
