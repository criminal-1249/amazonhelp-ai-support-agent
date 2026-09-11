from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

from retriever import get_retriever


def format_docs(documents):
    formatted_docs = []

    for doc in documents:
        customer_query = doc.page_content
        agent_reply = doc.metadata["agent_reply"]

        formatted_docs.append(
            f"Customer query: {customer_query}\n"
            f"Historical agent reply: {agent_reply}"
        )

    return "\n\n".join(formatted_docs)


def create_rag_chain():
    # 1. Get retriever
    retriever = get_retriever(k=3)

    # 2. Create LLM
    llm = ChatGroq(
        api_key= "sentence-transformers/all-MiniLM-L6-v2",
        model="llama-3.1-8b-instant",
        temperature=0
    )

    # 3. Create prompt
    prompt = ChatPromptTemplate.from_template(
        """
You are an Amazon customer support agent.

Your task is to draft a helpful response to the customer's message.

Use the historical Amazon support examples as evidence.

Rules:
- Base your response on the historical examples.
- Do not invent policies, refunds, guarantees, or procedures.
- Be concise and professional.
- If the historical examples are not sufficient to answer the issue,
  clearly indicate that the issue should be handled by a human support agent.

Historical support examples:
{context}

Customer message:
{question}

Draft a response:
"""
    )

    # 4. Create RAG chain
    chain = (
        {
            "context": retriever | format_docs,
            "question": lambda x: x
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain


if __name__ == "__main__":
    chain = create_rag_chain()

    question = "My Amazon order has not arrived yet. What should I do?"

    response = chain.invoke(question)

    print("\nCustomer:")
    print(question)

    print("\nAI Response:")
    print(response)