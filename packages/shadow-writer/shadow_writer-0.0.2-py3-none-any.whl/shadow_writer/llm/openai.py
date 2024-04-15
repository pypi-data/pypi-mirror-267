from openai import OpenAI


class OAI_client:
    """Generative AI model using OpenAI's API."""

    def __init__(self, api_key, model="gpt-4-0125-preview"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, messages, with_json_response_format: bool = False):
        """Generate a response based on the input messages."""

        if with_json_response_format:
            response = self.client.chat.completions.create(
                response_format={"type": "json_object"},
                messages=messages,
                model=self.model,
            )
        else:
            response = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
            )
        return response.choices[0].message.content
