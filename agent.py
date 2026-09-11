from src.agent.intent import classify_intent
from src.agent.response import generate_response
from src.agent.escalation import decide_escalation


def run_agent(customer_message):


    intent = classify_intent(customer_message)


    result = generate_response(
        customer_message=customer_message,
        intent=intent,
        k=3
    )

    response = result["response"]
    evidence = result["evidence"]


    escalation = decide_escalation(
        customer_message=customer_message,
        intent=intent,
        response=response,
        evidence=evidence
    )


    return {
        "customer_message": customer_message,
        "intent": intent,
        "response": response,
        "decision": escalation["decision"],
        "reason": escalation["reason"],
        "evidence": evidence
    }


# --------------------------------------------------
# Run application
# --------------------------------------------------

if __name__ == "__main__":

    print("=" * 70)
    print("AMAZON CUSTOMER SUPPORT AI AGENT")
    print("=" * 70)
    print("enter exit to exit the chat")
    while True:
        customer_message = input("\nCustomer: ")

        if customer_message.lower() == "exit":
            break
            
        result = run_agent(customer_message)

        print("\n" + "=" * 70)
        print("INTENT")
        print("=" * 70)
        print(result["intent"])

        print("\n" + "=" * 70)
        print("RESPONSE")
        print("=" * 70)
        print(result["response"])

        print("\n" + "=" * 70)
        print("ESCALATION")
        print("=" * 70)
        print("Decision:", result["decision"])
        print("Reason:", result["reason"])

        print("\n" + "=" * 70)
        print("EVIDENCE")
        print("=" * 70)

        for i, evidence in enumerate(result["evidence"], start=1):

            print(f"\nEvidence {i}")
            print("Customer:", evidence["customer_query"])
            print("Amazon Agent:", evidence["agent_reply"])
            print("Conversation ID:", evidence["conversation_id"])

            print("\n" + "=" * 70)