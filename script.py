import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import re

load_dotenv(find_dotenv())
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
model = "gpt-4o-mini"

line_range_regex = r"Change line (\d+)\s*-\s*(\d+)"
code_block_regex = r"```python\s*(.*?)```"
plantuml_block_regex = r"```plantuml\s*(.*?)```"

with open('prompt_2.txt', 'r') as file:
    content = file.read()

with open('calc.puml', 'r') as file_2:
    content += "```plantuml\n"
    content += file_2.read()
    content += "\n```"

messages = [
    {"role": "system", "content": "Embody the role of the most qualified subject matter experts and before answering my question inform me what role you are embodying."},
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

line_range_match = re.search(line_range_regex, answer)
code_block_match = re.search(code_block_regex, answer, re.DOTALL)
plantuml_block_match = re.search(plantuml_block_regex, answer, re.DOTALL)

if line_range_match and code_block_match:
    start_line = int(line_range_match.group(1))
    end_line = int(line_range_match.group(2))
    new_code = code_block_match.group(1).strip()

    print(f"Replacing lines {start_line}–{end_line} in calc.py...")

    new_code_lines = new_code.split("\n")

    with open('calc.py', 'r') as file:
        lines = file.readlines()


    expected_line_count = end_line - start_line + 1
    actual_line_count = len(new_code_lines)

    if actual_line_count < expected_line_count:
        print(f"Warning: Expected {expected_line_count} lines, but received {actual_line_count}. Extracting only available lines.")
    

    lines[start_line - 1:start_line - 1 + actual_line_count] = [line + "\n" for line in new_code_lines]

    with open('calc.py', 'w') as file:
        file.writelines(lines)

    print(f"Lines {start_line}–{start_line + actual_line_count - 1} have been replaced in calc.py.")
else:
    print("Failed to parse the response. Please check the response format.")

print("######################################################")
if plantuml_block_match:
    with open("calc.puml", "r") as file:
        plantuml_content = file.read().strip()

    if plantuml_content == plantuml_block_match.group(1).strip():
        print("PlantUML block is the same as the one in the response.")
    else:
        print("PlantUML block is different from the one in the response.")

print("######################################################")
print("messages: ", messages)
print("######################################################")
print("response: ", answer)
