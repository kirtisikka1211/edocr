import os
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class LlmInferencer:
    """
    various llms for inferencing
    """
    def __init__(self):
        self.groq_client = Groq(api_key=GROQ_API_KEY)

    def inference_groq(self, prompt: str)->str:
        """
        inference from groq
        ARGS:
            prompt str: prompt for llm
        Returns:
            response_msg str: response from llm
        """
        try:
            response = self.groq_client.chat.completions.create(
                model="deepseek-r1-distill-llama-70b",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
        except Exception as e:
            raise Exception(f"{str(e)}")
        response_msg = response.choices[0].message.content
        return response_msg
