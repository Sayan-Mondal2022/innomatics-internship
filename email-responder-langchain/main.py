from chains.intent_chain import intent_chain
from chains.response_chain import response_chain


def generate_response(email):
    # Step 1: intent classification
    intent = intent_chain.invoke({"email": email}).content.strip()

    # Step 2: response generation
    reply = response_chain.invoke({"email": email, "intent": intent}).content

    return intent, reply


if __name__ == "__main__":
    email = """
    Hi,
    I haven't received my refund yet.
    Please help.
    """

    intent, reply = generate_response(email)

    print("Intent:", intent)
    print("\nReply:\n", reply)
