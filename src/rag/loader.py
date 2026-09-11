from langchain_community.document_loaders import JSONLoader


def load_conversations(file_path):
    loader = JSONLoader(
        file_path=file_path,
        jq_schema=".",
        text_content=False,
        json_lines=True
    )

    documents = loader.load()

    print(f"Loaded {len(documents):,} conversations")

    return documents


if __name__ == "__main__":
    file_path = "data/processed/amazon_conversations_rag_based.jsonl"

    documents = load_conversations(file_path)

    print("\nFirst document:")
    print(documents[0].page_content)

    print("\nMetadata:")
    print(documents[0].metadata)