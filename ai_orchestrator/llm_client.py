import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def call_llm(prompt: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=2048
    )

    return response.choices[0].message.content

