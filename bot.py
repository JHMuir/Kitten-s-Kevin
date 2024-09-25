import brain
from dotenv import load_dotenv
import discord
from discord import app_commands
from icecream import ic

#load from .env
load_dotenv()
intents = discord.Intents.all()
intents.message_content = True

def should_reply(client: discord.Client, message: discord.Message) -> bool:
    # Checking if our bot should reply to a message
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
            # Preparing a message to send to Groq
            # print(message)
            prepared_message = (
                f'{message.author.nick + ":" + message.content.strip()}'
            )
            print(prepared_message)
            
            try:
                reply = await brain.reply(prepared_message)
                await message.reply(content = reply, mention_author = False)
                
            except Exception as e:
                ic(e)
                await message.reply(
                    "Meow! I'm sorry, something went wrong. Try again later!",
                    mention_author = False,
                )           