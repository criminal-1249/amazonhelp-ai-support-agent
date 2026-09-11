from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.rag.retriever import get_retriever

from dotenv import load_dotenv

load_dotenv()


MODEL_NAME = "openai/gpt-oss-20b"



def get_llm():

    return ChatGroq(
        model=MODEL_NAME,
        temperature=0
    )



def format_documents(documents):

    formatted = []

    for i, document in enumerate(
        documents,
        start=1
    ):

        customer_query = document.page_content

        agent_reply = document.metadata.get(
            "agent_reply",
            ""
        )

        formatted.append(
            f"""
Historical Example {i}

Customer:
{customer_query}

Amazon Agent:
{agent_reply}
"""
        )

    return "\n".join(formatted)


def generate_response(
    customer_message,
    intent,
    k=3
):

    # 1. Get retriever
    retriever = get_retriever(k=k)

    # 2. Retrieve similar historical cases
    documents = retriever.invoke(
        customer_message
    )

    # 3. Format historical evidence
    context = format_documents(
        documents
    )

    # 4. Get Groq LLM
    llm = get_llm()

    # 5. Prompt
    prompt = ChatPromptTemplate.from_template(
        """
You are an Amazon customer support agent.

Your task is to draft a helpful response to the
customer using the historical Amazon support examples.

Customer intent:
{intent}

Customer message:
{customer_message}

Historical Amazon support examples:
{context}

Rules:

1. Address the customer's actual problem.
2. Use the historical examples as evidence.
3. Do not invent Amazon policies or procedures.
4. Do not promise refunds, replacements, compensation,
   or other actions unless supported by the examples.
5. Do not mention that you are an AI.
6. Keep the response concise and professional.
7. If the historical examples are insufficient to
   safely answer the customer, indicate that human
   support is required.

Write ONLY the customer-facing response.
"""
    )

    # 6. Create chain
    chain = (
        prompt
        | llm
        | StrOutputParser()
    )

    # 7. Generate response
    response = chain.invoke({
        "intent": intent,
        "customer_message": customer_message,
        "context": context
    })

    # 8. Store evidence
    evidence = []

    for document in documents:

        evidence.append({
            "customer_query": document.page_content,
            "agent_reply": document.metadata.get(
                "agent_reply",
                ""
            ),
            "conversation_id": document.metadata.get(
                "conversation_id"
            )
        })

    # 9. Return complete result
    return {
        "intent": intent,
        "response": response.strip(),
        "evidence": evidence
    }

if __name__ == "__main__":

    customer_message = (
        "My Amazon package was supposed to arrive "
        "three days ago but I still haven't received it."
    )

    intent = "order_not_received"

    result = generate_response(
        customer_message,
        intent
    )

    print("\n" + "=" * 60)
    print("CUSTOMER")
    print("=" * 60)

    print(customer_message)

    print("\n" + "=" * 60)
    print("INTENT")
    print("=" * 60)

    print(result["intent"])

    print("\n" + "=" * 60)
    print("GENERATED RESPONSE")
    print("=" * 60)

    print(result["response"])

    print("\n" + "=" * 60)
    print("EVIDENCE")
    print("=" * 60)

    for i, evidence in enumerate(
        result["evidence"],
        start=1
    ):

        print(f"\nEvidence {i}")

        print(
            "Customer:",
            evidence["customer_query"]
        )

        print(
            "Agent:",
            evidence["agent_reply"]
        )