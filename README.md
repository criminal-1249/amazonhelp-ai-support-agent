# AmazonHelp AI Support Agent

An AI-powered customer support agent for **AmazonHelp** built using intent classification, RAG (Retrieval-Augmented Generation), and automatic human escalation.

## Important: Vector Store Generation

The FAISS vector store is **not included in this repository** because the generated index is too large for GitHub's standard file-size limits.

The project contains approximately **150,000 RAG chunks**. Generating the FAISS vector store requires embedding these chunks and may take some time:

* **CPU:** approximately **10–18 minutes**
* **GPU:** approximately **5–10 minutes**

**Please wait patiently while the vector store is being generated.** The exact time depends on your hardware and system configuration.

The vector store only needs to be generated once locally.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/criminal-1249/amazonhelp-ai-support-agent.git
cd amazonhelp-ai-support-agent
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the API key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Do not commit the `.env` file to GitHub.

## Generate the FAISS Vector Store

Before running the agent, generate the local vector store:

```bash
python -m src.rag.vector_store
```

This processes the historical AmazonHelp conversations, creates approximately **150,000 RAG chunks**, generates their embeddings, and builds the FAISS vector index.

The generated index will be saved under:

```text
data/vector_store/
```

You should see:

```text
FAISS vector store saved to: data/vector_store/amazon_faiss
```

The vector store is generated locally and is intentionally ignored by Git.

> **Note:** Vector-store generation is the longest step of the setup. Please allow approximately **10–18 minutes on CPU** or **5–10 minutes on GPU**.

## Run the Agent

Once the vector store has been generated, start the support agent:

```bash
python agent.py
```

You can then enter customer support messages interactively.

The agent performs the following steps:

1. **Intent Classification** — identifies the customer's support intent.
2. **RAG Retrieval** — retrieves relevant historical AmazonHelp conversations.
3. **Response Generation** — generates a response grounded in the retrieved historical examples.
4. **Escalation Decision** — determines whether the query should be:

   * `AUTO_HANDLE`
   * `HUMAN`

## Golden Set Evaluation

The repository contains a **golden evaluation set** under:

```text
eval/golden_eval.jsonl
```

To run the evaluation:

```bash
python eval/run_golden_eval.py
```

The evaluation script runs the agent on the golden examples and reports classification performance for the escalation decision.

It produces metrics including:

* Accuracy
* Macro Precision
* Macro Recall
* Macro F1
* Classification Report
* Confusion Matrix

The generated evaluation outputs are saved under:

```text
eval/
```

The evaluation result files are ignored by Git because they are generated locally.

### Verify the Golden Set

Before running the evaluation, you can inspect the golden set directly:

```bash
type eval/golden_eval.jsonl
```

On Linux/macOS:

```bash
cat eval/golden_eval.jsonl
```

Each entry contains a customer query and its expected escalation label, for example:

```json
{"id":1,"customer_query":"Where is my order?","gold_escalation":"AUTO_HANDLE"}
```

To verify the evaluation pipeline, run:

```bash
python eval/run_golden_eval.py
```

A successful run should display output similar to:

```text
Accuracy       : 0.XXXX
Macro Precision: 0.XXXX
Macro Recall   : 0.XXXX
Macro F1       : 0.XXXX

Classification Report:
...

Confusion Matrix
...
```

> **Note:** For the final assignment evaluation, the golden set should be treated as the held-out evaluation set and should not be used to modify or tune the agent.

## Quick Start

```bash
pip install -r requirements.txt

python -m src.rag.vector_store

python agent.py
```

To run the evaluation:

```bash
python eval/run_golden_eval.py
```

**Important:** If the vector store already exists in `data/vector_store/`, you do not need to generate it again. You can directly run:

```bash
python agent.py
```
