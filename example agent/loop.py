import json
import os

from dotenv import load_dotenv
from groq import Groq

from employee import get_balance, list_transactions, send_payment
from tools import tools


load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = "openai/gpt-oss-120b"
MAX_TOOL_ROUNDS = 5

client = Groq(api_key=GROQ_API_KEY)
functions = {
    "get_balance": get_balance,
    "send_payment": send_payment,
    "list_transactions": list_transactions,
}

messages = [{"role": "user", "content": input("You: ")}]

for _ in range(MAX_TOOL_ROUNDS):
    response = client.chat.completions.create(
        model=LLM_MODEL,
        tools=tools,
        messages=messages,
    )
    assistant_message = response.choices[0].message

    if not assistant_message.tool_calls:
        print(assistant_message.content or "")
        break

    messages.append(assistant_message.model_dump(exclude_unset=True))

    for tool_call in assistant_message.tool_calls:
        function = functions[tool_call.function.name]
        arguments = json.loads(tool_call.function.arguments)
        result = function(**arguments)
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result),
            }
        )
else:
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
    )
    print(response.choices[0].message.content or "")
