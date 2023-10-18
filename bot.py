from collections import defaultdict
import os
import palm
from dotenv import load_dotenv
from datetime import datetime
import discord
from discord import app_commands
from icecream import ic

#load from .env
load_dotenv()
LIMIT = int(os.getenv('MSG_LIMIT', 10))
intents = discord.Intents.all()
intents.message_content = True
channel_history = defaultdict(list[str])

def should_reply(client: discord.Client, message: discord.Message) -> bool:
    #checking if our bot should reply to a message
    if(
        message.author.bot
        or not message.channel.permissions_for(message.guild.me).send_messages
    ):
        return False
    
    return client.user.mentioned_in(message)

class KittensBot(discord.Client):
    def __init__(self) -> None:
        super().__init__(intents = intents)
        self.tree = discord.app_commands.CommandTree(self)
        
    async def on_ready(self: discord.Client):
        print(f'We have logged in as {self.user.name}(ID: {self.user.id}!')
        guild = discord.utils.get(self.guilds)
        print(f'{self.user} is connected to the following guilds:')
        for guild in self.guilds:
            print(f'{guild.name}(ID: {guild.id})')
        await self.tree.sync()
        print(f'{self.user} is ready.')
        
    async def on_message(self, message: discord.Message):
        if should_reply(self,message):
            #prepare and add to our message limit
            prepared_message = (
                f'{message.content.strip()}'
            )
            #check if limit reached
            if len(channel_history[message.channel.id]) >= LIMIT:
                channel_history[message.channel.id].clear()
            #insert into channel history
            channel_history[message.channel.id].append(prepared_message)
            
            try:
                reply = await palm.reply(channel_history[message.channel.id])
                bot_reply = f"{reply.strip()}"
                channel_history[message.channel.id].append(bot_reply)
                channel_history[message.channel.id].append("NEXT REQUEST")
                
                await message.reply(reply, mention_author = False)
            except Exception as e:
                ic(e)
                
                await message.reply(
                    "Meow! I'm sorry, something went wrong. Try again later!",
                    mention_author = False,
                )
                channel_history[message.channel.id].pop()
                