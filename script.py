import os, discord
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# allow bot to access guild members intents
intents = discord.Intents.default()
client = commands.Bot(command_prefix="$", intents=intents)

# set some variables
embed_title = "Roles Bot Command"
embed_colour = 0xE5E242

def check_message(message):
   return message[0:7]=="SUTOM #" and message[11:13]=="/6"

@client.event
async def on_ready():
   print("> Bot connected")

@client.event
async def on_message(message):
   if(check_message(message.content)):
      msg = message.content
      splitted = msg.split("\n")
      del splitted[0]
      if splitted[0]=="":
         del splitted[0]
      del splitted[-1]
      if splitted[-1]=="":
         del splitted[-1]
      tentatives = len(splitted)

@client.command(name="ranking")
async def roles(ctx, *args):
   await ctx.send("Bot triggered")

client.run(TOKEN)
