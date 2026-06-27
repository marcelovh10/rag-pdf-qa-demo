from typing import List
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from app.config import settings


def get_llm():
    if settings.llm_provider == "groq":
        return ChatGroq(
            model=settings.llm_model,
            api_key=settings.groq_api_key,
            temperature=0.0,
        )
    if settings.llm_provider == "anthropic":
        return ChatAnthropic(
            model=settings.llm_model,
            api_key=settings.anthropic_api_key,
        )
    return ChatOpenAI(
        model=settings.llm_model,
        openai_api_key=settings.openai_api_key,
    )


SYSTEM_PROMPT = """You are a precise assistant that answers questions using only the provided context.

RULES:
- Answer based ONLY on the context chunks provided.
- If the context doesn't contain the answer, say "I don't have that information in the provided documents."
- Cite your sources by referencing the chunk number in brackets, e.g. [1], [2].
- Be concise. Use bullet points when listing.
- Never invent information not in the context."""


def format_context(chunks: List[dict]) -> str:
    parts = []
    for i, chunk in enumerate(chunks, 1):
        page = chunk.get("metadata", {}).get("page", "?")
        source = chunk.get("metadata", {}).get("source", "unknown")
        parts.append(f"[Chunk {i}] (page {page}, source: {source}):\n{chunk['content']}")
    return "\n\n---\n\n".join(parts)


async def generate_answer(question: str, context_chunks: List[dict]) -> tuple[str, dict]:
    """Generate an answer with citations. Returns (answer, usage_metadata)."""
    llm = get_llm()
    context = format_context(context_chunks)
    user_msg = f"CONTEXT:\n{context}\n\nQUESTION: {question}"

    response = await llm.ainvoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=user_msg),
        ]
    )

    usage = {
        "input_tokens": response.usage_metadata.get("input_tokens", 0),
        "output_tokens": response.usage_metadata.get("output_tokens", 0),
    }
    return response.content, usage
