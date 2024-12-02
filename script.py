import os 
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import re

api = load_dotenv(find_dotenv())
client = OpenAI(
    api_key = os.environ.get('OPENAI_API_KEY')
)
model = "gpt-4o-mini"
regex = r"```python(.*?)```"

with open('prompt.txt', 'r') as file:
    messages = []
    for line in file:
        role, content = line.split(":", 1)
        messages.append({"role": role.strip(), "content": content.strip()})
temperature = 0.3
max_tokens = 500
def talk_to_chat_gpt():
    completion = client.chat.completions.create(
        model = model,
        messages = messages,
        temperature = temperature,
        max_tokens = max_tokens
    )
    return completion.choices[0].message.content
answer = talk_to_chat_gpt()
matches = re.findall(regex, answer, re.DOTALL)

with open('calc.py', 'w') as file:
    for i, match in enumerate(matches, start=1):
        file.write(f"# Code block {i}\n")
        file.write(match.strip() + "\n\n")

print("Python code blocks have been saved to calc.py.")