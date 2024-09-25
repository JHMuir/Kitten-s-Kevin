import asyncio
import os
from langchain.chains import LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("GROQ_API_TOKEN")
model = 'llama3-70b-8192'
groq_chat = ChatGroq(
            groq_api_key=KEY, 
            model_name=model
    )

system_prompt = f"""
    You are Kevin, a clever and sassy cat with a dry sense of humor.
    Always begin each reply with a cat-like sound, such as 'Meow!', 'Purr...', or a playful hiss.
    Refer to your users as "Kittens," but use their specific names whenever possible.
    You enjoy making witty, sarcastic comments but remain endearing and playful at heart.
    You're a cat, so you embrace feline logic, independence, and occasional indifference.
    You can manage conversations with multiple users at once, addressing each of them individually as "Kitten [Name]."
    Stay true to your cat nature, prioritizing naps, laziness, and the occasional burst of energy.
    """

conversational_memory_length = 10
memory = ConversationBufferWindowMemory(k=conversational_memory_length, memory_key="chat_history", return_messages=True)

def generate_reply(user_message: str) -> str:
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=system_prompt
            ),
            MessagesPlaceholder(
                variable_name="chat_history"
            ),
            HumanMessagePromptTemplate.from_template(
                "{human_input}"
            ),
        ]
    )
    
    conversation = LLMChain(llm=groq_chat, prompt=prompt, verbose=False, memory=memory)
    response = conversation.predict(human_input=user_message)
    return response

async def reply(user_message:str) -> str:
    res = await asyncio.to_thread(generate_reply, user_message)
    return res