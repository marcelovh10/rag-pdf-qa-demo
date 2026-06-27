-- Drop everything and recreate with 384d
drop table if exists document_chunks cascade;
drop function if exists match_chunks cascade;
drop index if exists document_chunks_embedding_idx;
drop index if exists document_chunks_document_id_idx;

create extension if not exists vector;

create table document_chunks (
  id uuid primary key,
  document_id uuid not null,
  content text not null,
  embedding vector(384) not null,
  metadata jsonb default '{}'::jsonb,
  created_at timestamp with time zone default now()
);

create index document_chunks_embedding_idx
  on document_chunks
  using ivfflat (embedding vector_cosine_ops)
  with (lists = 100);

create index document_chunks_document_id_idx
  on document_chunks (document_id);

create or replace function match_chunks(
  query_embedding vector(384),
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

select 'recreated 384d' as status;