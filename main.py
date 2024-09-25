import os
import random
from dotenv import load_dotenv
from bot import *

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN is None:
    raise EnvironmentError('TOKEN is not set!')

client = KittensBot()

client.run(TOKEN)