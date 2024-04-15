from usellm import Message, Options, UseLLM


def np(question):
    response = generate_response(question)
    print(response)
    """

    print(code)

def np(message):
    # Initialize the service
    service = UseLLM(service_url="https://usellm.org/api/llm")

    # Prepare the conversation
    messages = [
        Message(role="system", content="You are a helpful assistant."),
        Message(role="user", content=message),
    ]
    options = Options(messages=messages)

    # Interact with the service
    response = service.chat(options)

    # Return the assistant's response
    return response.content
