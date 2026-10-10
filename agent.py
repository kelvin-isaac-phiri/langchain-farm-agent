import os
import sys

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from db import DB_PATH, init_db
from tools import (
    get_farm_info,
    get_crop_information,
    check_farm_weather,
    search_web,
)


load_dotenv()

if not os.getenv("GOOGLE_API_KEY") and not os.getenv("GEMINI_API_KEY"):
    print(
        "Missing API key. Add GOOGLE_API_KEY to a .env file.\n"
        "Get a free key: https://aistudio.google.com/apikey"
    )
    sys.exit(1)

init_db()

tools = [
    get_farm_info,
    get_crop_information,
    check_farm_weather,
    search_web,
]

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
)

graph = create_agent(model, tools)


def print_tool_trace(messages) -> None:
    """Show tools used on the latest turn — helpful for learning."""
    # Only look at messages after the most recent user question.
    last_human = 0
    for i, message in enumerate(messages):
        if isinstance(message, HumanMessage):
            last_human = i

    used_tools = False

    for message in messages[last_human + 1 :]:
        if isinstance(message, AIMessage) and message.tool_calls:
            used_tools = True
            for call in message.tool_calls:
                print(f"  → tool: {call['name']}({call.get('args', {})})")

        if isinstance(message, ToolMessage):
            preview = str(message.content).replace("\n", " ")
            if len(preview) > 120:
                preview = preview[:117] + "..."
            print(f"  ← result: {preview}")

    if not used_tools:
        print("  (no tools used)")


if __name__ == "__main__":

    print("🌱 AgriGuide")
    print("Educational AI farm agent (LangChain + Gemini + tools + SQLite)")
    print(f"Database: {DB_PATH.name}")
    print()
    print("Sample farm IDs: F001 (maize, Lilongwe) | F002 (tomato, Dedza)")
    print("Type 'quit' to exit.")
    print()

    farm_id = input("Farm ID: ").strip() or "F001"

    system_message = SystemMessage(
        content=f"""
You are AgriGuide, a simple agricultural decision-support agent.

The farmer's farm ID is {farm_id}.
Valid demo farms are F001 and F002.

Use tools when helpful:
- Farm details come from the agent_db SQLite database (farms table).
- Use search_web for outside farming guidance when local tools are not enough.
Combine farm/weather data with web results when relevant.
Do not invent farm information.
Give practical and easy-to-understand advice.
Cite web sources briefly when you used search_web.
Do not claim to make a definite diagnosis.
If information is insufficient, say what else should be checked.
"""
    )

    messages = [system_message]

    while True:
        question = input("\nYour question: ").strip()

        if not question:
            continue

        if question.lower() in {"quit", "exit", "q"}:
            print("Goodbye.")
            break

        messages.append(HumanMessage(content=question))

        result = graph.invoke({"messages": messages})
        messages = result["messages"]

        print("\n🔧 Tools used:")
        print_tool_trace(messages)

        print("\n🤖 AgriGuide:")
        print(messages[-1].text)
