import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_response(prompt, history=None, model_name="gpt-3.5-turbo", history_length=3):
    """
    Get a response from the OpenAI model using conversation history.
    
    Args:
        prompt: The current user prompt
        history: List of previous (prompt, response) tuples
        model_name: Model to use (default: gpt-3.5-turbo)
        history_length: How many past interactions to include
    
    Returns:
        The model's response as a string.
    """
    if history is None:
        history = []

    # Construct chat history
    messages = []
    for user, assistant in history[-history_length:]:
        messages.append({"role": "user", "content": user})
        messages.append({"role": "assistant", "content": assistant})
    messages.append({"role": "user", "content": prompt})

    try:
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=messages
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[ERROR] {e}"

def run_chat(model_name="gpt-3.5-turbo", history_length=3):
    """
    Run an interactive chat session that maintains context.
    """
    print("Contextual LLM Chat\nType 'exit' to quit.")
    history = []

    try:
        while True:
            try:
                user_input = input("\nYou: ")
            except EOFError:
                print("\n[EOF received] Exiting...")
                break

            if user_input.lower().strip() == "exit":
                print("Goodbye!")
                break

            response = get_response(user_input, history, model_name, history_length)
            print(f"ChatGPT: {response}")

            # Track the conversation
            history.append((user_input, response))

    except KeyboardInterrupt:
        print("\n[Interrupted with Ctrl+C — exiting]")

if __name__ == "__main__":
    run_chat()
