from langchain_community.vectorstores import FAISS

from .loader import load_conversations
from .chunker import create_rag_chunks
from .embeddings import get_embeddings, create_embeddings


DATA_PATH = "data/processed/amazon_conversations_rag_based.jsonl"
VECTOR_STORE_PATH = "data/vector_store/amazon_faiss"


def create_vector_store():
    documents = load_conversations(DATA_PATH)

    rag_chunks = create_rag_chunks(documents)

    embeddings = get_embeddings()

    # Create embeddings with progress tracking
    vectors = create_embeddings(
        rag_chunks,
        embeddings,
        batch_size=100
    )

    # Create FAISS store from existing embeddings
    vector_store = FAISS.from_embeddings(
        text_embeddings=[
            (document.page_content, vector)
            for document, vector in zip(rag_chunks, vectors)
        ],
        embedding=embeddings
    )

    vector_store.save_local(VECTOR_STORE_PATH)

    print(f"\nFAISS vector store saved to: {VECTOR_STORE_PATH}")

    return vector_store


def load_vector_store():
    embeddings = get_embeddings()

    vector_store = FAISS.load_local(
        VECTOR_STORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    print("FAISS vector store loaded successfully")

    return vector_store


if __name__ == "__main__":
    create_vector_store()