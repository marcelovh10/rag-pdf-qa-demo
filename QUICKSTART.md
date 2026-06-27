# RAG PDF QA — Quick start (TL;DR)

## 0. Pick your provider combo (free options)

| Combo | Cost | Quality | Setup |
|---|---|---|---|
| **Groq + OpenAI embeddings** (recommended) | ~$0.02/1M tokens (~$1 total) | High | Easy |
| **Groq + HuggingFace local** (100% free) | $0 | Medium | Slower first run (downloads model) |
| **OpenAI everything** | ~$0.50-2/1M tokens | Highest | Easiest |
| **Anthropic + OpenAI** | $1-5/1M tokens | Highest | Easy |

**Recommended for first run:** Groq + OpenAI embeddings.

---

## 1. Set up Supabase (5 min)

1. Create project at https://supabase.com
2. Go to **SQL Editor** → New query
3. Paste contents of `supabase/migrations/0001_init_pgvector.sql` → Run
4. Copy **Project URL** and **service_role key** (Settings → API)

## 2. Get API keys (5 min)

- **Groq** (free): https://console.groq.com → API Keys → Create
- **OpenAI** (cheap): https://platform.openai.com → API Keys → Create (load $5 minimum)

## 3. Run backend (2 min)

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
notepad .env   # paste: GROQ_API_KEY, OPENAI_API_KEY, SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY
uvicorn app.main:app --reload --port 8000
```

Test: open http://localhost:8000/health → should return `{"status":"ok","llm":"groq/llama-3.3-70b-versatile"}`

## 4. Run frontend (2 min)

```bash
cd frontend
npm install
copy .env.example .env.local
# Edit .env.local with NEXT_PUBLIC_API_URL=http://localhost:8000
npm run dev
```

Open http://localhost:3000 → upload a PDF, ask a question.

## 5. Deploy (15 min)

### Backend → Railway
- railway.app → New project → Deploy from GitHub
- Set root: `rag-demo/backend/`
- Add env vars from `.env`
- Deploy → grab public URL

### Frontend → Vercel
- vercel.com → New project → Import repo
- Set root: `rag-demo/frontend/`
- Add env: `NEXT_PUBLIC_API_URL=<railway-url>`
- Deploy

Done. URL pública funcional en ~25 min desde cero.

## 6. Share on Upwork

- Replace portfolio placeholder with deployed URL.
- Take 2-3 screenshots: upload screen, question + answer, citations panel.
- Pin the live URL in your Upwork bio and proposals.
