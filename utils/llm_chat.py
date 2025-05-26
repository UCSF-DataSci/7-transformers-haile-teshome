import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def query(message, model="gpt-3.5-turbo", api_key=None):
    """
    Send a prompt to the OpenAI ChatGPT API.

    Args:
        message (str): The user's input prompt.
        model (str): The model to use (default: gpt-3.5-turbo).
        api_key (str): Optional override for the OpenAI API key.

    Returns:
        str: The model's response.
    """
    if api_key:
        openai.api_key = api_key

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": message}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"[Error] {str(e)}"

def run_chat(model="gpt-3.5-turbo"):
    """
    Run an interactive one-off chat session.
    Each input is treated independently (no memory).
    """
    print("One-Off Chat — type 'exit' to quit.")

    try:
        while True:
            try:
                user_input = input("\nYou: ").strip()
            except EOFError:
                print("\n[EOF received] Exiting...")
                break

            if user_input.lower() == "exit":
                print("Goodbye!")
                break

            response = query(user_input, model=model)
            print(f"ChatGPT: {response}")

    except KeyboardInterrupt:
        print("\n[Interrupted with Ctrl+C — exiting]")

if __name__ == "__main__":
    run_chat()
