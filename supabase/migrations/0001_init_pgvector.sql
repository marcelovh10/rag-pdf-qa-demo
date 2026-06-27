-- pgvector extension + RAG schema
-- Run this in Supabase SQL Editor
-- IMPORTANT: vector dimension must match your EMBEDDING_MODEL:
--   - OpenAI text-embedding-3-small / text-embedding-3-large: 1536
--   - HuggingFace sentence-transformers/all-MiniLM-L6-v2: 384
--   - HuggingFace BAAI/bge-small-en-v1.5: 384
--   - HuggingFace BAAI/bge-large-en-v1.5: 1024
-- Default below is 1536 (OpenAI). Edit if you use HuggingFace.

create extension if not exists vector;

create table if not exists document_chunks (
  id uuid primary key,
  document_id uuid not null,
  content text not null,
  embedding vector(1536) not null,
  metadata jsonb default '{}'::jsonb,
  created_at timestamp with time zone default now()
);

create index if not exists document_chunks_embedding_idx
  on document_chunks
  using ivfflat (embedding vector_cosine_ops)
  with (lists = 100);

create index if not exists document_chunks_document_id_idx
  on document_chunks (document_id);

-- RPC function: cosine similarity search with optional document filter
create or replace function match_chunks(
  query_embedding vector(1536),
  match_count int default 5,
  filter_document_id uuid default null
)
returns table (
  id uuid,
  document_id uuid,
  content text,
  metadata jsonb,
  similarity float
)
language plpgsql
as $$
begin
  return query
  select
    dc.id,
    dc.document_id,
    dc.content,
    dc.metadata,
    1 - (dc.embedding <=> query_embedding) as similarity
  from document_chunks dc
  where filter_document_id is null or dc.document_id = filter_document_id
  order by dc.embedding <=> query_embedding
  limit match_count;
end;
$$;
