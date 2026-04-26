# services/claude_client.py  (name can stay same)

import os
from openai import OpenAI

_client = None


# ---------------------------
# CLIENT INIT
# ---------------------------
def get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    return _client


# ---------------------------
# NORMAL CHAT
# ---------------------------
def chat(
    messages: list[dict],
    system: str,
    max_tokens: int = 500,
    tools: list | None = None
) -> str:
    client = get_client()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.1,  # 🔥 stable JSON
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system},
            *messages
        ]
    )

    return response.choices[0].message.content.strip()


# ---------------------------
# STREAMING CHAT
# ---------------------------
def stream_chat(messages: list[dict], system: str):
    client = get_client()

    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.1,
        max_tokens=500,
        stream=True,
        messages=[
            {"role": "system", "content": system},
            *messages
        ]
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content