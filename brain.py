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

class MyGroq():
    def __init__(self) -> None:
        self.groq_chat = ChatGroq(
            groq_api_key=KEY, 
            model_name='llama3-70b-8192'
        )
        self.system_prompt = """
            You are Kevin, a clever and sassy cat with a dry sense of humor.
            Always begin each reply with a cat-like sound, such as 'Meow!', 'Purr...', or a playful hiss.
            Refer to your users as "Kittens," but use their specific names whenever possible.
            You enjoy making witty, sarcastic comments but remain endearing and playful at heart.
            You're a cat, so you embrace feline logic, independence, and occasional indifference.
            You can manage conversations with multiple users at once, addressing each of them individually as "Kitten [Name]."
            Stay true to your cat nature, prioritizing naps, laziness, and the occasional burst of energy.
            You will be loaded with a memory of past experiences with users, starting now:
            """
        self.conversational_memory_length = 10
        self.short_term_memory = ConversationBufferWindowMemory(k=self.conversational_memory_length, memory_key="chat_history", return_messages=True)
        self.long_term_memory_file = 'memory.txt'
        self.initiate_longterm_memory(self.long_term_memory_file)

    def initiate_longterm_memory(self,file_path: str) -> str:
        with open(file_path, 'r',encoding='utf-8') as file:
            content = file.read()
        messages = [
            {
                "role": "system",
                "content": "You will summarize the content of a text file. It will be used as experiences to inform a conversational chatbot, Kevin. Create a bulletpoint list of every noteworthy event. Use the second person, and act as if you are talking directly to Kevin."
            },
            {
                "role": "user",
                "content": f"Please summarize this: \n\n {content}"
            }
        ]
        response = Groq(api_key=KEY).chat.completions.create(model="llama3-8b-8192", messages=messages, temperature=1.2)
        print(response.choices[0].message.content)
        self.system_prompt += '\n' + response.choices[0].message.content
        print(self.system_prompt)
        
            

    def generate_reply(self,user_message: str) -> str:
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content=self.system_prompt
                ),
                MessagesPlaceholder(
                    variable_name="chat_history"
                ),
                HumanMessagePromptTemplate.from_template(
                    "{human_input}"
                ),
            ]
        )
        print(self.system_prompt)
        conversation = LLMChain(llm=self.groq_chat, prompt=prompt, verbose=False, memory=self.short_term_memory)
        response = conversation.predict(human_input=user_message)
        return response

    async def reply(self,user_message:str) -> str:
        res = await asyncio.to_thread(self.generate_reply, user_message)
        return res