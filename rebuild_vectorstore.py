
import os

from langchain_community.vectorstores import FAISS
from rag_pipeline import get_embedding_model
from pdf_processor import load_and_split_pdf


if __name__ == "__main__":

    pdf_path = "data/sample.pdf"

    print("Starting OCR-based PDF processing...")

    pages, chunks = load_and_split_pdf(pdf_path)

    print("\nLoading embedding model...")

    embeddings = get_embedding_model()

    print("\nCreating updated FAISS database...")

    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    os.makedirs("vectorstore", exist_ok=True)

    vector_store.save_local("vectorstore")

    print("\nFAISS database successfully rebuilt!")

    print(f"Total pages: {len(pages)}")
    print(f"Total chunks: {len(chunks)}")
