import openai

def get_structured_response(prompt):
    function_def = [
        {
            "name": "extract_diagnosis",
            "parameters": {
                "type": "object",
                "properties": {
                    "diagnosis": {"type": "string"},
                    "confidence": {"type": "number"},
                    "reasoning": {"type": "string"}
                },
                "required": ["diagnosis", "confidence", "reasoning"]
            }
        }
    ]

    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-1106",
        messages=[{"role": "user", "content": prompt}],
        functions=function_def,
        function_call={"name": "extract_diagnosis"}
    )

    return response["choices"][0]["message"]["function_call"]["arguments"]
