from langchain_huggingface import HuggingFaceEmbeddings


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def get_embeddings():
    embeddings = HuggingFaceEmbeddings(
        model_name= "sentence-transformers/all-MiniLM-L6-v2"
    )

    return embeddings


def create_embeddings(rag_chunks, embeddings, batch_size=100):
    all_embeddings = []

    for i in range(0, len(rag_chunks), batch_size):
        batch = rag_chunks[i:i + batch_size]

        texts = [
            document.page_content
            for document in batch
        ]

        batch_embeddings = embeddings.embed_documents(texts)

        all_embeddings.extend(batch_embeddings)

        print(
            f"Processed {min(i + batch_size, len(rag_chunks)):,}"
            f"/{len(rag_chunks):,}"
        )

    print(f"\nCreated {len(all_embeddings):,} embeddings")
    print(f"Embedding dimension: {len(all_embeddings[0])}")

    return all_embeddings


if __name__ == "__main__":
    from loader import load_conversations
    from chunker import create_rag_chunks

    file_path = "data/processed/amazon_conversations_rag_based.jsonl"

    documents = load_conversations(file_path)

    rag_chunks = create_rag_chunks(documents)

    embeddings = get_embeddings()

    vectors = create_embeddings(
        rag_chunks,
        embeddings,
        batch_size=100
    )