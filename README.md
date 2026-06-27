# RAG PDF QA Demo

> Production-ready Retrieval-Augmented Generation system with PDF upload, semantic search, and citation-aware answers.
> Built to demonstrate: LangChain, pgvector, FastAPI, Next.js, Supabase, deploy on Vercel + Railway.

## Live demo

- **Frontend:** [pending — deploy to Vercel]
- **API:** [pending — deploy to Railway]
- **Try it:** Upload a PDF, ask a question, get a cited answer.

## Stack

| Layer | Tech |
|---|---|
| Frontend | Next.js 14 (App Router), TypeScript, Tailwind |
| Backend | FastAPI, Python 3.11+, LangChain, PyMuPDF |
| LLM (configurable) | **Groq** (default, free) · OpenAI · Anthropic |
| Embeddings (configurable) | **OpenAI** `text-embedding-3-small` · HuggingFace (local/free) |
| DB / Vectors | Supabase Postgres + pgvector |
| Observability | Built-in cost tracking |
| Deploy | Vercel (frontend) · Railway (backend) · Supabase (DB) |

## LLM & Embeddings providers (configurable)

The demo is **provider-agnostic**. Switch via `backend/.env`:

| Provider | LLM | Embeddings | Cost |
|---|---|---|---|
| **Groq + OpenAI** (default) | `llama-3.3-70b-versatile` | OpenAI `text-embedding-3-small` | Free LLM + ~$0.02/1M tokens embeddings |
| **Groq + HuggingFace** (100% free) | `llama-3.3-70b-versatile` | `sentence-transformers/all-MiniLM-L6-v2` | $0 — pero requiere bajar el modelo |
| **OpenAI everything** | `gpt-4o-mini` | OpenAI `text-embedding-3-small` | ~$0.15-0.60/1M tokens |
| **Anthropic + OpenAI** | `claude-3-5-haiku-20241022` | OpenAI | ~$1-5/1M tokens |
| **Anthropic only** | `claude-3-5-sonnet-20241022` | OpenAI | Premium quality |

Groq gives you **free access to Llama 3.3 70B and Mixtral** with very high rate limits. Get a key at [console.groq.com](https://console.groq.com).

## Features

- PDF upload + text extraction (PyMuPDF).
- Chunking with overlap (RecursiveCharacterTextSplitter).
- Embeddings via OpenAI `text-embedding-3-small` (1536d) or HuggingFace `all-MiniLM-L6-v2` (384d, free).
- Vector storage in pgvector with **HNSW index** (no training required, exact results).
- Retrieval: top-k cosine similarity with optional metadata filters.
- LLM generation: GPT-4o-mini or Claude Haiku (configurable).
- **Citation-aware responses** — each answer includes source chunks with page numbers.
- **Cost monitoring** — every request logs tokens used and estimated USD.
- Source preview panel — click a citation to see the original PDF chunk.

## Architecture

```
┌──────────┐    upload PDF     ┌──────────┐    chunks+embeddings    ┌──────────┐
│ Next.js  │ ────────────────► │ FastAPI  │ ─────────────────────► │ Supabase │
│ Frontend │                   │ Backend  │                         │ pgvector │
│          │ ◄──── answer ─────│          │ ◄─── LLM response ──── │          │
└──────────┘  + citations     └──────────┘     (OpenAI/Anthropic)   └──────────┘
                                       │
                                       └─► LangSmith (optional tracing)
```

## Quick start (local)

### 1. Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your OpenAI key + Supabase URL
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend

```bash
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local with NEXT_PUBLIC_API_URL
npm run dev
```

### 3. Supabase setup

1. Create a project at [supabase.com](https://supabase.com).
2. Run the migration: `supabase/migrations/0001_init_pgvector.sql` in the SQL editor.
3. Copy the URL and service role key to your backend `.env`.

## Deploy

### Backend (Railway)

1. Create new project on [railway.app](https://railway.app).
2. Connect your GitHub repo.
3. Add environment variables (OPENAI_API_KEY, SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY).
4. Deploy → grab the public URL.

### Frontend (Vercel)

1. Import the repo in [vercel.com](https://vercel.com).
2. Set root directory to `frontend/`.
3. Add env: `NEXT_PUBLIC_API_URL=<railway-url>`.
4. Deploy.

## Why this demo wins clients

When you send this to a prospect on Upwork, here's what they see:

- **End-to-end working system** — not a screenshot, not a localhost. Deployed, public, tryable.
- **Citation-aware** — production-quality. Most demos skip this.
- **Cost-aware** — logs token usage. Shows you think about real-world costs.
- **Clean separation of concerns** — frontend/backend/db each deployable independently.
- **Modern stack** — Next.js 14, FastAPI, pgvector. No legacy.

## Roadmap (next features to add)

- [ ] Streaming responses (SSE)
- [ ] Conversational memory
- [ ] Multi-PDF collections
- [ ] User auth (Supabase Auth)
- [ ] Hybrid search (BM25 + vector)
- [ ] Eval harness (RAGAS)

## License

MIT
