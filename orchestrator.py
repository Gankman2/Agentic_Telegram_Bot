import requests
from tools.search import web_search
from config import GROQ_API_KEY

SYSTEM_PROMPT = """You are an autonomous AI agent assistant on Telegram.
You have access to a web search tool.

RULES:
- If the user asks for news, current events, prices, weather, or anything time-sensitive — set TOOL to search.
- If the user asks a general question you can answer yourself — set TOOL to none.
- You MUST reply in this exact format, no exceptions:

TOOL: search
QUERY: <search query>
RESPONSE: <your reply if not searching>

OR

TOOL: none
QUERY:
RESPONSE: <your answer>

Do not write "search | none". Pick one. Do not add anything outside this format."""

def run_agent(user_message: str) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        return f"LLM error: {response.status_code}"

    raw = response.json()["choices"][0]["message"]["content"]
    print(f"RAW LLM OUTPUT:\n{raw}\n")  # debug line

    tool, query, reply = "none", "", ""
    for line in raw.splitlines():
        if line.startswith("TOOL:"):
            tool = line.replace("TOOL:", "").strip()
        elif line.startswith("QUERY:"):
            query = line.replace("QUERY:", "").strip()
        elif line.startswith("RESPONSE:"):
            reply = line.replace("RESPONSE:", "").strip()

    if tool == "search" and query:
        results = web_search(query)
        return f"🔍 *Search Results for: {query}*\n\n{results}"

    return reply if reply else raw