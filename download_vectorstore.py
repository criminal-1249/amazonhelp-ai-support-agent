from huggingface_hub import snapshot_download
import os

REPO_ID = "karthik0701/amazonhelp-faiss"
LOCAL_DIR = "data/vector_store/amazon_faiss"

os.makedirs(LOCAL_DIR, exist_ok=True)

snapshot_download(
    repo_id=REPO_ID,
    repo_type="dataset",
    local_dir=LOCAL_DIR,
    token=os.getenv("HF_TOKEN")
)

print("FAISS vector store downloaded successfully.")