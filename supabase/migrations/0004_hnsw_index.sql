-- Switch from IVFFlat to HNSW (no training required, exact results)
drop index if exists document_chunks_embedding_idx;

create index document_chunks_embedding_idx
  on document_chunks
  using hnsw (embedding vector_cosine_ops);

select 'switched to hnsw' as status;