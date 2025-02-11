import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import re

load_dotenv(find_dotenv())
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
model = "gpt-4o-mini"

code_block_regex = r"```python\s*(.*?)```"
plantuml_block_regex = r"```plantuml\s*(.*?)```"

with open('append_prompt.txt', 'r') as file:
    content = file.read()

with open('calc.puml', 'r') as file_2:
    content += "```plantuml\n"
    content += file_2.read()
    content += "\n```"

messages = [
    {"role": "system", "content": "Embody the role of the most qualified subject matter experts."},
    {"role": "user", "content": content}
]

def talk_to_chat_gpt():
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.2,
        max_tokens=500
    )
    return completion.choices[0].message.content

answer = talk_to_chat_gpt()
with open("response.txt", "a") as file:
    file.write(answer + "\n")

code_block_match = re.search(code_block_regex, answer, re.DOTALL)
plantuml_block_match = re.search(plantuml_block_regex, answer, re.DOTALL)

if code_block_match:
    new_code = code_block_match.group(1).strip()
    print(f"Appending new code in calc.py at the marker...")
    new_code_lines = new_code.split("\n")

    with open('calc.py', 'r') as file:
        lines = file.readlines()
    
    marker = "# Append new methods here"
    for i, line in enumerate(lines):
        if marker in line.strip():  
            insert_line = i + 1
            lines[insert_line:insert_line] = [line + "\n" for line in new_code_lines]
            with open('calc.py', 'w') as file:
                file.writelines(lines)
            print("New code has been appended at the marker in calc.py.")
            break
    else:
        print(f"Error: Marker '{marker}' not found in calc.py.")
else:
    print("Failed to parse the Python code block. Please check the response format.")

if plantuml_block_match:
    new_plantuml = plantuml_block_match.group(1).strip()
    with open('calc.puml', 'w') as file:
        file.write(new_plantuml + "\n")
    print("PlantUML block has been updated in calc.puml.")
else:
    print("Failed to parse the PlantUML block. Please check the response format.")

print("######################################################")
print("messages: ", messages)
print("######################################################")
print("response: ", answer)
