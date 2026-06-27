import uuid
import tempfile
import os
from typing import List
from fastapi import UploadFile
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from app.config import settings
from app.embeddings import get_embeddings
from app.db import get_supabase


def _extract_pdf_text(file_path: str) -> List[Document]:
    loader = PyMuPDFLoader(file_path)
    return loader.load()


def _split_documents(docs: List[Document]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        add_start_index=True,
    )
    return splitter.split_documents(docs)


async def ingest_pdf(file: UploadFile, document_id: str | None = None) -> str:
    """Ingest a PDF: extract → chunk → embed → store in pgvector.

    Returns the document_id used to group chunks together.
    """
    document_id = document_id or str(uuid.uuid4())
    sb = get_supabase()
    embeddings = get_embeddings()

    tmp_dir = tempfile.gettempdir()
    file_path = os.path.join(tmp_dir, f"{document_id}.pdf")
    try:
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        docs = _extract_pdf_text(file_path)
        chunks = _split_documents(docs)

        texts = [c.page_content for c in chunks]
        vectors = embeddings.embed_documents(texts)

        rows = []
        for chunk, vector in zip(chunks, vectors):
            rows.append(
                {
                    "id": str(uuid.uuid4()),
                    "document_id": document_id,
                    "content": chunk.page_content,
                    "embedding": vector,
                    "metadata": {
                        "page": chunk.metadata.get("page", 0),
                        "source": file.filename or "uploaded.pdf",
                    },
                }
            )

        sb.table("document_chunks").insert(rows).execute()
        return document_id
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
