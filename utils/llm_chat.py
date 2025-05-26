#!/usr/bin/env python3
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

class LLMClient:
    def __init__(self, model="gpt-3.5-turbo", api_key=None):
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if self.api_key:
            openai.api_key = self.api_key
        self.openai = openai

    def query(self, message):
        """
        Send a prompt to the OpenAI ChatGPT API.

        Args:
            message (str): The user's input prompt.

        Returns:
            str: The model's response.
        """
        if not self.openai.api_key:
            return "[Error] No API key found. Please set OPENAI_API_KEY."

        try:
            response = self.openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": message}]
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[Error] {str(e)}"

class LLMChatTool:
    """
    Wrapper class required by the autograder.
    Uses LLMClient internally.
    """
    def __init__(self, model="gpt-3.5-turbo"):
        self.client = LLMClient(model=model)

    def get_response(self, prompt):
        return self.client.query(prompt)

def run_chat(model="gpt-3.5-turbo"):
    """
    Run an interactive one-off chat session.
    Each input is treated independently (no memory).
    """
    client = LLMClient(model=model)

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

            response = client.query(user_input)
            print(f"ChatGPT: {response}")

    except KeyboardInterrupt:
        print("\n[Interrupted with Ctrl+C — exiting]")


def main():
    run_chat()

if __name__ == "__main__":
    main()
