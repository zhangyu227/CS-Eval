import os
import openpyxl
from typing import List, Tuple
from openai import OpenAI

client = OpenAI(api_key="sk-4466e198a55946ad8716d27615c5bd84", base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)

print(response.choices[0].message.content)