from functools import lru_cache
from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from app.config import settings


@lru_cache
def get_embeddings():
    if settings.embedding_provider == "huggingface":
        kwargs = {"model_name": settings.embedding_model}
        if settings.huggingface_api_key:
            kwargs["api_key"] = settings.huggingface_api_key
        return HuggingFaceEmbeddings(**kwargs)

    # default: openai
    return OpenAIEmbeddings(
        model=settings.embedding_model,
        openai_api_key=settings.openai_api_key,
    )
