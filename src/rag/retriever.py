from .vector_store import load_vector_store


def get_retriever(k=3):
    vector_store = load_vector_store()

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )

    return retriever


if __name__ == "__main__":
    retriever = get_retriever(k=3)

    query = "My Amazon order has not arrived yet"

    results = retriever.invoke(query)

    print(f"\nFound {len(results)} similar cases\n")

    for i, document in enumerate(results, start=1):
        print(f"--- Result {i} ---")

        print("Customer:")
        print(document.page_content)

        print("\nHistorical Agent Reply:")
        print(document.metadata["agent_reply"])

        print("\nConversation ID:")
        print(document.metadata["conversation_id"])

        print()