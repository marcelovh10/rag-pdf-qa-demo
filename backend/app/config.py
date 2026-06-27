from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    openai_api_key: str = ""
    anthropic_api_key: str | None = None
    groq_api_key: str | None = None
    huggingface_api_key: str | None = None

    supabase_url: str
    supabase_service_role_key: str

    llm_provider: str = "groq"
    llm_model: str = "llama-3.3-70b-versatile"
    embedding_provider: str = "openai"
    embedding_model: str = "text-embedding-3-small"
    embedding_dim: int = 1536

    chunk_size: int = 800
    chunk_overlap: int = 150
    retrieval_top_k: int = 5

    cors_origins: str = "http://localhost:3000"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",")]


settings = Settings()
