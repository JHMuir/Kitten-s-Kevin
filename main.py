import os
import random
from dotenv import load_dotenv
from bot import *

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN is None:
    raise EnvironmentError('TOKEN is not set!')

client = KittensBot()
bullyDict = {}

#=====creating custom commands=====
#FF14 prompt
@client.tree.command(name='ff14', description= "Informs the heathens of the greatness of FF14")
async def FinalFantasy(interaction):
    response =  f"""
        Did you know the critically acclaimed MMORPG FINAL FANTASY XIVs starter edition 
        and free trial now include the entirety of A Realm Reborn, the award-winning Heavensward, and its second major expansion Stormblood? 
        A grand adventure awaits, now up to level 70!
    """
    await interaction.response.send_message(response)

#FF14 UwUized
@client.tree.command(name='ff14uwu', description= "omg i wove catgiwls!!")
async def FinalFantasyUwU(interaction):
    response = f"""
        Did uwu know thawt the cwiticawwy accwaimed MMOWPG finaw fantasy xiv has a fwee twiaw, 
        thwat incwudes the entiwety of A Weawm Webown, the awawd-winning Heavenswawd expansion, and wits secownd wexpansion Stwormbwood up tuwu wevew 70 with no westwictions own pwaytime? 
        sign up, awnd enjoy Eowzea today!
    """
    await interaction.response.send_message(response)

client.run(TOKEN)
