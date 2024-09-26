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
from groq import Groq
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

def initiate_longterm_memory():
    with open('memory.txt', 'r',encoding='utf-8') as file:
        content = file.read()
    messages = [
        {
            "role": "system",
            "content": "You will summarize the content of a text file. It will be used as experiences to inform a conversational chatbot. Detail every noteworthy event using bulletpoints, including what has happened to Kevin or who has spoken to him. Use the second person, and act as if you are talking directly to Kevin."
        },
        {
            "role": "user",
            "content": f"Please summarize this: \n\n {content}"
        }
    ]
    response = Groq(api_key=KEY).chat.completions.create(model="llama3-8b-8192", messages=messages, temperature=1.2)
    
    print(response.choices[0].message.content)
        

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