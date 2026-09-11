from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = "openai/gpt-oss-20b"


def get_llm():

    return ChatGroq(
        model=MODEL_NAME,
        temperature=0
    )



def decide_escalation(
    customer_message,
    intent,
    response,
    evidence
):

    # Convert evidence into text
    evidence_text = ""

    for i, item in enumerate(
        evidence,
        start=1
    ):

        evidence_text += f"""
Evidence {i}

Customer:
{item["customer_query"]}

Amazon Agent:
{item["agent_reply"]}

"""


  

    prompt = ChatPromptTemplate.from_template(
        """
You are an Amazon customer support escalation classifier.

Your job is to decide whether a customer support request
can be safely handled automatically or should be escalated
to a human support agent.

Customer message:
{customer_message}

Detected intent:
{intent}

Draft response:
{response}

Historical evidence:
{evidence}

Decision rules:

1. AUTO_HANDLE
Use AUTO_HANDLE when:
- The issue is simple and well supported by the historical
  examples.
- The response can safely guide the customer.
- No sensitive account-specific investigation is required.
- No uncertain or unsupported action is being promised.

2. HUMAN
Use HUMAN when:
- The historical evidence is insufficient.
- The issue requires account/order-specific investigation.
- The customer is asking for an action that cannot safely
  be completed from the available information.
- The situation is ambiguous or unusually complex.
- The draft response itself says human support is required.

Return EXACTLY this format:

DECISION: AUTO_HANDLE
REASON: short explanation

OR

DECISION: HUMAN
REASON: short explanation

Do not provide anything else.
"""
    )



    chain = (
        prompt
        | get_llm()
        | StrOutputParser()
    )


    result = chain.invoke({
        "customer_message": customer_message,
        "intent": intent,
        "response": response,
        "evidence": evidence_text
    })




    result = result.strip()

    if result.startswith("DECISION: AUTO_HANDLE"):

        decision = "AUTO_HANDLE"

    elif result.startswith("DECISION: HUMAN"):

        decision = "HUMAN"

    else:

        # Safe fallback
        decision = "HUMAN"


    # Extract reason
    reason = ""

    if "REASON:" in result:

        reason = result.split(
            "REASON:",
            1
        )[1].strip()

    return {
        "decision": decision,
        "reason": reason
    }




if __name__ == "__main__":

    customer_message = (
        "My Amazon package was supposed to arrive "
        "three days ago but I still haven't received it."
    )

    intent = "order_not_received"

    response = (
        "I'm sorry your package has not arrived yet. "
        "Please check the delivery information for your order."
    )

    evidence = [
        {
            "customer_query": "My package hasn't arrived.",
            "agent_reply": (
                "Please check the tracking information "
                "for your order."
            ),
            "conversation_id": 123
        }
    ]

    result = decide_escalation(
        customer_message,
        intent,
        response,
        evidence
    )

    print("\n" + "=" * 60)
    print("ESCALATION DECISION")
    print("=" * 60)

    print("Decision:", result["decision"])
    print("Reason:", result["reason"])