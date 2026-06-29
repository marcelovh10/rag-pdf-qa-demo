"""Embeddings provider with auto-fallback.

Primary config comes from EMBEDDING_PROVIDER env var (openai | huggingface).
If OpenAI is configured but no API key is available, automatically fall back
to HuggingFace local embeddings. This prevents the app from crashing if env
vars are misconfigured.
"""
from functools import lru_cache
from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from app.config import settings


@lru_cache
def get_embeddings():
    provider = settings.embedding_provider
    has_openai_key = bool(settings.openai_api_key and settings.openai_api_key.strip())

    # Auto-fallback: if OpenAI is requested but no key, use HuggingFace
    if provider == "openai" and not has_openai_key:
        import logging
        logging.warning(
            "EMBEDDING_PROVIDER=openai but OPENAI_API_KEY is empty. "
            "Falling back to HuggingFace local embeddings."
        )
        provider = "huggingface"

    if provider == "huggingface":
        kwargs = {"model_name": settings.embedding_model}
        if settings.huggingface_api_key:
            kwargs["api_key"] = settings.huggingface_api_key
        return HuggingFaceEmbeddings(**kwargs)

    return OpenAIEmbeddings(
        model=settings.embedding_model,
        openai_api_key=settings.openai_api_key,
    )
