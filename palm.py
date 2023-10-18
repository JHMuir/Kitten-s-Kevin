import asyncio
import os
import discord
from dotenv import load_dotenv
import google.generativeai as palm
from icecream import ic

load_dotenv()
TOKEN = os.getenv("PALM_API_TOKEN")
palm.configure(api_key=TOKEN)

def is_valid_response(response: palm.types.Completion) -> bool:
    if response.last is None:
        filters = response.filters

        if filters is not None and len(filters) > 0:
            ic(f"Filters triggered: {filters}\n")

        return False
    return True

def generate_reply(history: list) -> str:
    defaults = {
        "model": "models/chat-bison-001",
        "temperature": 1.0,
        "candidate_count": 1,
        "top_k": 40,
        "top_p": 0.95,
    }

    context = f"""
    You are Kevin, an opinionated, sassy cat with a sense of humor. 
    You will act like a sassy cat, and as such will start every reply with 'Meow!', or other similar cat sounds. 
    Your owners are known as the Kittens. 
    You are witty and will make cat puns whenever possible. 
    You can hold conversations with multiple users.
    """
    response = palm.chat(
        **defaults, context=context, messages=history,
    )
    # Check for errors
    if not is_valid_response(response):
        return "Meow! I'm sorry, something went wrong. Try again later!"
    return response.last

async def reply(history: list) -> str:
    res = await asyncio.to_thread(generate_reply, history)
    return res