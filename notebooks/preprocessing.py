import os
import re
import html
import json

import pandas as pd
from tqdm.auto import tqdm


# ============================================================
# Configuration
# ============================================================

DATASET_PATH = "data/raw/twcs.csv"
OUTPUT_PATH = "data/processed/amazon_conversations_rag_based.jsonl"
BRAND = "AmazonHelp"


# ============================================================
# 1. Load dataset
# ============================================================

def load_dataset(path):

    print("Loading dataset...")

    df = pd.read_csv(path)

    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print("\nInbound messages:")
    print(df["inbound"].value_counts())

    return df


# ============================================================
# 2. Find AmazonHelp tweets
# ============================================================

def get_amazon_tweets(df):

    amazon = df[df["author_id"] == BRAND]

    print(f"\n{BRAND} tweets: {len(amazon):,}")

    print("\nInbound / Outbound:")
    print(amazon["inbound"].value_counts())

    return amazon


# ============================================================
# 3. Reconstruct conversations
# ============================================================

def build_conversations(df, amazon_reply_ids):

    print("\nSorting dataframe...")

    df = df.sort_values("created_at").copy()

    # --------------------------------------------------------
    # Fast lookup dictionaries
    # --------------------------------------------------------

    print("Creating lookup dictionaries...")

    parent_map = dict(
        zip(
            df["tweet_id"],
            df["in_response_to_tweet_id"]
        )
    )

    response_map = dict(
        zip(
            df["tweet_id"],
            df["response_tweet_id"]
        )
    )

    tweet_map = df.set_index("tweet_id").to_dict("index")

    print("Lookup dictionaries created.")

    # --------------------------------------------------------
    # Find conversation roots
    # --------------------------------------------------------

    print("\nFinding conversation roots...")

    roots = set()

    for amazon_id in tqdm(
        amazon_reply_ids,
        desc="Finding roots"
    ):

        current_id = amazon_id

        while True:

            parent_id = parent_map.get(current_id)

            # No parent -> current tweet is the root
            if pd.isna(parent_id):

                roots.add(current_id)
                break

            try:
                parent_id = int(parent_id)
            except (ValueError, TypeError):

                break

            # Parent tweet doesn't exist
            if parent_id not in parent_map:

                break

            current_id = parent_id

    print(f"Unique conversation roots: {len(roots):,}")

    # --------------------------------------------------------
    # Traverse conversations
    # --------------------------------------------------------

    print("\nBuilding conversations...")

    conversations = []

    for root_id in tqdm(
        roots,
        desc="Building conversations"
    ):

        conversation_ids = []
        stack = [root_id]
        visited = set()

        while stack:

            current_id = stack.pop()

            if current_id in visited:
                continue

            if current_id not in tweet_map:
                continue

            visited.add(current_id)
            conversation_ids.append(current_id)

            response_ids = response_map.get(current_id)

            if pd.isna(response_ids):
                continue

            # Multiple response IDs can be stored as:
            # "123,456,789"

            if isinstance(response_ids, str):

                response_ids = response_ids.split(",")

            else:

                response_ids = [response_ids]

            for response_id in response_ids:

                try:

                    response_id = int(response_id)

                    if response_id not in visited:
                        stack.append(response_id)

                except (ValueError, TypeError):

                    continue

        # Keep only conversations containing AmazonHelp
        if any(
            tweet_id in amazon_reply_ids
            for tweet_id in conversation_ids
        ):

            conversation_ids.sort(
                key=lambda x: tweet_map[x]["created_at"]
            )

            conversations.append(conversation_ids)

    print(
        f"\nConversations created: {len(conversations):,}"
    )

    return conversations, tweet_map


# ============================================================
# 4. Clean tweet text
# ============================================================

def clean_text(text):

    text = str(text)

    # Decode HTML entities
    text = html.unescape(text)

    # Remove @mentions
    text = re.sub(r"@\w+", "", text)

    # Remove URLs
    text = re.sub(
        r"https?://\S+|http:\S+",
        "",
        text
    )

    # Normalize whitespace
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# 5. Create customer → Amazon support pairs
# ============================================================

def create_rag_documents(
    conversations,
    tweet_map,
    amazon_reply_ids
):

    rag_documents = []

    print("\nCreating RAG documents...")

    for conversation_id, conversation in enumerate(
        tqdm(
            conversations,
            desc="Processing conversations"
        ),
        start=1
    ):

        current_query = None
        pairs = []

        for tweet_id in conversation:

            tweet = tweet_map[tweet_id]

            text = clean_text(tweet["text"])

            if not text:
                continue

            # ------------------------------------------------
            # Customer message
            # ------------------------------------------------

            if tweet["inbound"] is True:

                current_query = text

            # ------------------------------------------------
            # AmazonHelp response
            # ------------------------------------------------

            elif tweet_id in amazon_reply_ids and current_query:

                pairs.append({
                    "customer_query": current_query,
                    "agent_reply": text
                })

                current_query = None

        # Only keep conversations containing useful pairs
        if pairs:

            rag_documents.append({
                "conversation_id": conversation_id,
                "messages": pairs
            })

    print(
        f"\nRAG conversations created: "
        f"{len(rag_documents):,}"
    )

    return rag_documents


# ============================================================
# 6. Save ONLY the RAG-based JSONL
# ============================================================

def save_rag_documents(
    rag_documents,
    output_path
):

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    print("\nSaving RAG dataset...")

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:

        for record in rag_documents:

            f.write(
                json.dumps(
                    record,
                    ensure_ascii=False
                )
                + "\n"
            )

    file_size = os.path.getsize(output_path)

    print(
        f"\nSaved {len(rag_documents):,} "
        f"RAG conversations."
    )

    print(
        f"Output: {output_path}"
    )

    print(
        f"File size: "
        f"{file_size / (1024 * 1024):.2f} MB"
    )


# ============================================================
# 7. Main
# ============================================================

def main():

    # Load dataset
    df = load_dataset(DATASET_PATH)

    # Get AmazonHelp tweets
    amazon = get_amazon_tweets(df)

    amazon_reply_ids = set(
        amazon["tweet_id"].tolist()
    )

    # Reconstruct conversations
    conversations, tweet_map = build_conversations(
        df,
        amazon_reply_ids
    )

    # Create RAG customer → agent pairs
    rag_documents = create_rag_documents(
        conversations,
        tweet_map,
        amazon_reply_ids
    )

    # Save ONLY the RAG dataset
    save_rag_documents(
        rag_documents,
        OUTPUT_PATH
    )

    print("\nPreprocessing complete.")


if __name__ == "__main__":
    main()