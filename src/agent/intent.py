import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


load_dotenv()

INTENTS = {
    "order_not_received":
        "Customer says an ordered item has not arrived or is missing.",

    "delivery_delay":
        "Customer says delivery is late, delayed, or taking longer than promised.",

    "delivery_tracking":
        "Customer asks about tracking, shipment status, or where the package currently is.",

    "delivery_attempt_issue":
        "Customer says delivery was falsely attempted, the driver could not deliver, or delivery instructions were ignored.",

    "wrong_or_missing_item":
        "Customer received the wrong item, an incomplete order, an empty package, or an item different from what was ordered.",

    "damaged_product":
        "Customer received a damaged, broken, defective, or poor-quality product.",

    "return_issue":
        "Customer wants to return an item or has a problem with the return process or pickup.",

    "refund_issue":
        "Customer is waiting for a refund or has a problem with a refund after a return or cancellation.",

    "order_cancellation":
        "Customer wants to cancel an order or reports that an order was cancelled.",

    "payment_issue":
        "Customer has a problem with payment, card charges, payment failures, duplicate charges, or billing.",

    "account_issue":
        "Customer has a problem accessing, securing, or using their Amazon account.",

    "seller_issue":
        "Customer has a problem specifically involving a third-party seller.",

    "product_information":
        "Customer asks about a product, feature, availability, compatibility, pricing, or product-related information.",

    "stock_availability":
        "Customer asks whether a product is in stock or when an out-of-stock product will become available.",

    "digital_or_app_issue":
        "Customer reports a problem with an Amazon app, Prime Video, digital content, device, code, or other digital service.",

    "customer_support_issue":
        "Customer reports difficulty contacting support, getting a response, receiving a promised callback, or getting their issue resolved.",

    "shipping_or_delivery_question":
        "Customer asks a general question about delivery dates, delivery companies, shipping options, or delivery policies.",

    "other":
        "The message does not clearly fit any of the defined support intents."
}

def get_llm():
    return ChatGroq(
        model= "openai/gpt-oss-20b",
        temperature=0
    )



def create_intent_chain():

    llm = get_llm()

    intent_list = "\n".join(
        f"- {name}: {description}"
        for name, description in INTENTS.items()
    )

    prompt = ChatPromptTemplate.from_template(
        """
You are an Amazon customer support intent classifier.

Classify the customer's message into EXACTLY ONE
of the allowed intents below.

Allowed intents:
{intents}

Rules:
- Choose exactly one intent.
- Do not create a new intent.
- Use the customer's main problem.
- Return ONLY the intent name.
- Do not provide an explanation.

Customer message:
{customer_message}

Intent:
"""
    )

    chain = (
        prompt
        | llm
        | StrOutputParser()
    )

    return chain, intent_list


def classify_intent(customer_message):

    chain, intent_list = create_intent_chain()

    result = chain.invoke({
        "intents": intent_list,
        "customer_message": customer_message
    })

    intent = result.strip()

    # Safety check: make sure LLM returned a valid intent
    if intent not in INTENTS:
        return "other"

    return intent


if __name__ == "__main__":

    test_messages = [
        "i recived the damaged product",
        "i love this product but i accidently purchased it so i dont want this product",
        "i am not good with the product",
        "i like foods"
    ]

    for message in test_messages:

        intent = classify_intent(message)

        print("\nCustomer:")
        print(message)

        print("Intent:")
        print(intent)