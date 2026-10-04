from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
LAST_N_MESSAGE = os.getenv("LAST_N_MESSAGE")


async def get_response(history, provider: str = "groq"):
    if provider == "groq":
        client = AsyncOpenAI(
            base_url=os.getenv("GROQ_BASE_URL"), api_key=os.getenv("GROQ_API_KEY")
        )
        model = "llama-3.3-70b-versatile"
    elif provider == "gemini":
        client = AsyncOpenAI(
            base_url=os.getenv("GEMINI_BASE_URL"), api_key=os.getenv("GEMINI_API_KEY")
        )
        model = "gemini-3.5-flash-lite"

    else:
        raise ValueError(f"Unknown Provider: {provider}")
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {"content": m.content, "role": m.role} for m in history[:LAST_N_MESSAGE]
        ],
    )
    return response.choices[0].message.content
