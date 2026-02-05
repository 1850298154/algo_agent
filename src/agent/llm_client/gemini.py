from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
) 

gemini_3_flash_preview_model ="gemini-3-flash-preview"


"""
https://ai.google.dev/gemini-api/docs/models
https://aistudio.google.com/app/api-keys
"""



if __name__ == "__main__":
    response = client.chat.completions.create(
        model="gemini-3-flash-preview",
        # model="gemini-3-pro-preview",
        messages=[
            {   "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                # "content": "Explain to me how AI works."
                "content": "10个字内简单回答什么是ai"
            }
        ]
    )

    print(response.choices[0].message)  