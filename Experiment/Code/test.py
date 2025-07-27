import os
import openpyxl
from typing import List, Tuple
from openai import OpenAI

client = OpenAI(api_key="", base_url="")

response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)

print(response.choices[0].message.content)
