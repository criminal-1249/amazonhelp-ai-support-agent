# AmazonHelp AI Support Agent

An AI-powered customer support agent for **AmazonHelp** built using intent classification, RAG (Retrieval-Augmented Generation), and automatic human escalation.

## Important: Vector Store Not Included

The FAISS vector store is **not included in this repository** because the generated index is too large for GitHub's standard file-size limits.

You need to generate the vector store locally before running the agent.

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

This processes the available conversation data and creates the FAISS index under:

```text
data/vector_store/
```

The vector store is generated locally and is ignored by Git.

## Run the Agent

Once the vector store has been created, start the support agent:

```bash
python agent.py
```

You can then enter customer support messages interactively.

The agent performs the following steps:

1. Classifies the customer's intent.
2. Retrieves relevant historical AmazonHelp conversations using RAG.
3. Generates a response grounded in the retrieved examples.
4. Decides whether the query should be:

   * `AUTO_HANDLE`
   * `HUMAN`


## Quick Start

```bash
pip install -r requirements.txt

python -m src.rag.vector_store

python agent.py
```

**Note:** The vector-store generation step only needs to be performed when the local FAISS index is not already present.
