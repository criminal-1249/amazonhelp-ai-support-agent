import json
import random
import time
from collections import Counter

from tqdm import tqdm

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from src.rag.loader import load_conversations
from src.rag.chunker import create_rag_chunks




DATA_PATH = "data/processed/amazon_conversations_rag_based.jsonl"

MODEL_NAME = "qwen2.5:1.5b"

SAMPLE_SIZE = 1000      
BATCH_SIZE = 5

OUTPUT_FILE = "data/processed/intent_classified.jsonl"


llm = ChatOllama(
    model=MODEL_NAME,
    temperature=0
)


def classify_batch(messages):

    numbered_messages = "\n".join(
        f"{i}: {message}"
        for i, message in enumerate(messages)
    )

    prompt = f"""
You are analyzing Amazon customer support messages.

Identify the MAIN customer-support intent for every message.

Rules:
- Classify based on the customer's actual problem.
- Similar problems should use the same intent.
- Do not create extremely specific intents.
- Use short snake_case intent names.
- Do not include explanations.
- Return exactly one intent for every message.
- Return exactly {len(messages)} results.
- Do not skip any message.

Possible intent examples:

order_not_received
order_cancellation
refund_issue
payment_issue
damaged_product
wrong_product
account_issue
delivery_issue
seller_issue
product_issue
other

These are only examples.
You may create another meaningful intent if necessary.

Customer messages:

{numbered_messages}

Return ONLY valid JSON using this format:

[
    {{
        "id": 0,
        "intent": "example_intent"
    }},
    {{
        "id": 1,
        "intent": "example_intent"
    }}
]
"""

    response = llm.invoke(prompt)

    content = response.content

    return json.loads(content)




def load_customer_queries():

    print("Loading conversations...")

    documents = load_conversations(DATA_PATH)

    print("Creating RAG chunks...")

    rag_chunks = create_rag_chunks(documents)

    messages = [
        chunk.page_content
        for chunk in rag_chunks
    ]

    print(
        f"Total customer queries: {len(messages):,}"
    )

    return messages




def main():

  

    messages = load_customer_queries()



    random.seed(42)

    if len(messages) < SAMPLE_SIZE:
        raise ValueError(
            f"Only {len(messages)} messages available."
        )

    sampled_messages = random.sample(
        messages,
        SAMPLE_SIZE
    )

    print(
        f"Randomly selected "
        f"{len(sampled_messages):,} messages"
    )


    results = []

    total_batches = (
        len(sampled_messages) + BATCH_SIZE - 1
    ) // BATCH_SIZE

    print(
        f"Processing {total_batches:,} batches..."
    )

    with tqdm(
        total=total_batches,
        desc="Classifying",
        unit="batch"
    ) as progress:

        for start in range(
            0,
            len(sampled_messages),
            BATCH_SIZE
        ):

            batch = sampled_messages[
                start:start + BATCH_SIZE
            ]

            try:

                classifications = classify_batch(batch)

                if len(classifications) != len(batch):

                    print(
                        f"\nWarning: expected "
                        f"{len(batch)} results but got "
                        f"{len(classifications)}"
                    )

                    continue


                for message, classification in zip(
                    batch,
                    classifications
                ):

                    results.append({
                        "customer_query": message,
                        "intent": classification["intent"]
                    })

                progress.update(1)

            except Exception as e:

                print(
                    f"\nError in batch "
                    f"{start // BATCH_SIZE + 1}: {e}"
                )

                time.sleep(2)



    print("\nSaving results...")

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        for result in results:

            f.write(
                json.dumps(
                    result,
                    ensure_ascii=False
                ) + "\n"
            )


    intent_counts = Counter(
        result["intent"]
        for result in results
    )

    print("\n" + "=" * 60)
    print("INTENT DISTRIBUTION")
    print("=" * 60)

    for intent, count in intent_counts.most_common():

        percentage = (
            count / len(results)
        ) * 100

        print(
            f"{intent:35} "
            f"{count:6,} "
            f"({percentage:.2f}%)"
        )

    print("\n" + "=" * 60)

    print(
        f"Successfully classified: "
        f"{len(results):,}/"
        f"{len(sampled_messages):,}"
    )

    print(
        f"Results saved to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()