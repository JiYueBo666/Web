from openai import OpenAI
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.session import get_client
from prompt.math_helper import summarize_prompt


def summarize(text, client=None):
    if client is None:
        client = get_client()
    response = client.chat.completions.create(
        model="qwen-turbo",
        messages=[
            {"role": "system", "content": summarize_prompt},
            {"role": "user", "content": text},
        ],
        max_tokens=300,
    )
    return response.choices[0].message.content

