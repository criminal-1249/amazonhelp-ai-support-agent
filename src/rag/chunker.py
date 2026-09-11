import json
from tqdm import tqdm
from langchain_core.documents import Document


def create_rag_chunks(documents):
    chunks = []

    for doc in tqdm(documents, desc="Creating RAG chunks", unit="conversation"):
        conversation = json.loads(doc.page_content)

        conversation_id = conversation["conversation_id"]

        for message in conversation["messages"]:
            customer_query = message["customer_query"].strip()
            agent_reply = message["agent_reply"].strip()

            # Skip incomplete pairs
            if not customer_query or not agent_reply:
                continue

            chunk = Document(
                page_content=customer_query,
                metadata={
                    "conversation_id": conversation_id,
                    "agent_reply": agent_reply
                }
            )

            chunks.append(chunk)

    print(f"Created {len(chunks):,} RAG chunks")

    return chunks


if __name__ == "__main__":
    from loader import load_conversations

    file_path = "data/processed/amazon_conversations_rag_based.jsonl"

    documents = load_conversations(file_path)

    rag_chunks = create_rag_chunks(documents)

    print("\nFirst RAG chunk:")
    print("Customer:", rag_chunks[0].page_content)
    print("Agent:", rag_chunks[0].metadata["agent_reply"])
    print("Conversation ID:", rag_chunks[0].metadata["conversation_id"])