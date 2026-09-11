from langchain_community.vectorstores import FAISS

from .loader import load_conversations
from .chunker import create_rag_chunks
from .embeddings import get_embeddings, create_embeddings


DATA_PATH = "data/processed/amazon_conversations_rag_based.jsonl"
VECTOR_STORE_PATH = "data/vector_store/amazon_faiss"


def create_vector_store():
    # 1. Load conversations
    documents = load_conversations(DATA_PATH)

    # 2. Create RAG documents
    rag_chunks = create_rag_chunks(documents)

    # 3. Load embedding model
    embeddings = get_embeddings()

    # 4. Create embeddings in batches
    vectors = create_embeddings(
        rag_chunks,
        embeddings,
        batch_size=100
    )

    # 5. Create FAISS store
    #
    # IMPORTANT:
    # from_embeddings() needs both the text/embedding pairs
    # AND the metadata.
    text_embeddings = [
        (document.page_content, vector)
        for document, vector in zip(rag_chunks, vectors)
    ]

    metadatas = [
        document.metadata
        for document in rag_chunks
    ]

    vector_store = FAISS.from_embeddings(
        text_embeddings=text_embeddings,
        embedding=embeddings,
        metadatas=metadatas
    )

    # 6. Save FAISS index
    vector_store.save_local(VECTOR_STORE_PATH)

    print(
        f"\nFAISS vector store saved to: "
        f"{VECTOR_STORE_PATH}"
    )

    return vector_store


def load_vector_store():
    # Load the same embedding model used to create the index
    embeddings = get_embeddings()

    # Load the existing FAISS index
    vector_store = FAISS.load_local(
        VECTOR_STORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    print("FAISS vector store loaded successfully")

    return vector_store


if __name__ == "__main__":
    create_vector_store()