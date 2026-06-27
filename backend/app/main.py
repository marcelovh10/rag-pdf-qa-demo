"""FastAPI app entry point."""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.embeddings import Embeddings
from app.config import settings
from app.db import get_supabase
from app.embeddings import get_embeddings
from app.ingest import ingest_pdf
from app.rag import generate_answer
from app.schemas import IngestResponse, QueryRequest, QueryResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting RAG API. LLM=%s/%s, embedding=%s", settings.llm_provider, settings.llm_model, settings.embedding_model)
    yield
    logger.info("Shutting down")


app = FastAPI(
    title="RAG PDF QA API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _estimate_cost(usage: dict) -> float:
    """Rough USD cost estimate. Adjust to your actual provider pricing."""
    pricing_per_million = {
        # OpenAI
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-4-turbo": {"input": 10.00, "output": 30.00},
        # Anthropic
        "claude-3-5-haiku-20241022": {"input": 1.00, "output": 5.00},
        "claude-3-5-sonnet-20241022": {"input": 3.00, "output": 15.00},
        "claude-3-opus-20240229": {"input": 15.00, "output": 75.00},
        # Groq (free tier, but shown for reference)
        "llama-3.3-70b-versatile": {"input": 0.59, "output": 0.79},
        "llama-3.1-8b-instant": {"input": 0.05, "output": 0.08},
        "llama-3.1-70b-versatile": {"input": 0.59, "output": 0.79},
        "mixtral-8x7b-32768": {"input": 0.24, "output": 0.24},
    }
    p = pricing_per_million.get(settings.llm_model, {"input": 0.15, "output": 0.60})
    cost = usage["input_tokens"] * p["input"] / 1_000_000 + usage["output_tokens"] * p["output"] / 1_000_000
    return round(cost, 6)


@app.get("/health")
async def health():
    return {"status": "ok", "llm": f"{settings.llm_provider}/{settings.llm_model}"}


@app.post("/ingest", response_model=IngestResponse)
async def ingest_endpoint(file: UploadFile = File(...)):
    """Upload a PDF, extract, chunk, embed, store."""
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files are supported")

    document_id = await ingest_pdf(file)
    sb = get_supabase()
    count_result = sb.table("document_chunks").select("id", count="exact").eq("document_id", document_id).execute()

    return IngestResponse(
        document_id=document_id,
        chunks_created=count_result.count or 0,
        filename=file.filename,
    )


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(req: QueryRequest):
    """Ask a question. Returns answer with citations and cost estimate."""
    embeddings = get_embeddings()
    sb = get_supabase()

    query_vector = embeddings.embed_query(req.question)
    top_k = req.top_k or settings.retrieval_top_k

    rpc_params = {
        "query_embedding": query_vector,
        "match_count": top_k,
    }
    if req.document_id:
        rpc_params["filter_document_id"] = req.document_id

    try:
        result = sb.rpc("match_chunks", rpc_params).execute()
        chunks = result.data or []
    except Exception as e:
        logger.exception("Vector search failed")
        raise HTTPException(500, f"Vector search failed: {e}")

    if not chunks:
        return QueryResponse(
            answer="I don't have any documents indexed yet. Please upload a PDF first.",
            citations=[],
            usage={"input_tokens": 0, "output_tokens": 0},
            estimated_cost_usd=0.0,
        )

    answer, usage = await generate_answer(req.question, chunks)
    citations = [
        {
            "chunk_id": c["id"],
            "content": c["content"],
            "page": c.get("metadata", {}).get("page"),
            "source": c.get("metadata", {}).get("source"),
            "score": c.get("similarity", 0.0),
        }
        for c in chunks
    ]

    return QueryResponse(
        answer=answer,
        citations=citations,
        usage=usage,
        estimated_cost_usd=_estimate_cost(usage),
    )
