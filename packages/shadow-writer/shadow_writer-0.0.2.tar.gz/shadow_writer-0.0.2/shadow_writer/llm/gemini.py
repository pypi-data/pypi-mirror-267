import google.generativeai as genai


class Gemini_client:
    """Generative AI model using Google's GenerativeAI API."""

    def __init__(self, api_key, model="gemini-1.5-pro-latest"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

    def generate(self, messages):
        """Generate a response based on the input messages."""
        assert (
            len(messages) == 2
        ), "Requires exactly 2 messages (instruction and user request) to generate a response."
        prompt = (
            f"{messages[0]['content']}\n\n Task Description\n: {messages[1]['content']}"
        )
        response = self.model.generate_content(prompt)
        return response.text
