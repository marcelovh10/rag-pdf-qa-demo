// API client for RAG backend.
// API_URL is injected at build time from NEXT_PUBLIC_API_URL env var.
// Fallback to localhost only for local dev (npm run dev).

const API_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  (typeof window !== "undefined" && window.location.hostname === "localhost"
    ? "http://localhost:8000"
    : "https://rag-pdf-qa-demo-production.up.railway.app");

export type Citation = {
  chunk_id: string;
  content: string;
  page: number | null;
  source: string | null;
  score: number;
};

export type QueryResponse = {
  answer: string;
  citations: Citation[];
  usage: { input_tokens: number; output_tokens: number };
  estimated_cost_usd: number;
};

export type IngestResponse = {
  document_id: string;
  chunks_created: number;
  filename: string;
};

export async function ingestPdf(file: File): Promise<IngestResponse> {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${API_URL}/ingest`, { method: "POST", body: form });
  if (!res.ok) throw new Error(`Ingest failed: ${res.statusText}`);
  return res.json();
}

export async function query(question: string, documentId?: string): Promise<QueryResponse> {
  const res = await fetch(`${API_URL}/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, document_id: documentId }),
  });
  if (!res.ok) throw new Error(`Query failed: ${res.statusText}`);
  return res.json();
}

export async function health(): Promise<{ status: string; llm: string }> {
  const res = await fetch(`${API_URL}/health`);
  return res.json();
}
