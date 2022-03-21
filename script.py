import os, discord, json
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# allow bot to access guild members intents
intents = discord.Intents.default()
client = commands.Bot(command_prefix="$", intents=intents)

# set some variables
embed_title = "Motus Games Bot"
embed_colour = 0xE5E242
filename = "./data/sutom.json"
# filename = "/home/pi/Documents/MotusGamesBot/data/sutom.json"

def check_message(message):
   if(message[0:7]=="SUTOM #" and message[11:13]=="/6"):
      return "sutom"
   elif(message=="$ranking"):
      return "ranking"
   else:
      return None

def store_obj(obj):
   with open(filename, "r") as f:
      stored = json.load(f)
   stored.append(obj)
   with open(filename, "w") as f:
      json.dump(stored, f, indent=3, separators=(',', ': '))

def get_points(tentatives):
   if tentatives == 1:
      return 25
   elif tentatives == 2:
      return 20
   elif tentatives == 3:
      return 15
   elif tentatives == 4:
      return 10
   elif tentatives == 5:
      return 5
   else:
      return 0

def check_if_already_sent(author):
   with open(filename, "r") as f:
      stored = json.load(f)
   for obj in stored:
      if obj["pseudo"] == author:
         return True
   return False

def create_embed(desc):
   return discord.Embed(
      title=embed_title,
      colour=embed_colour,
      description=desc
   )

def process_message(message):
   splitted = message.split("\n")
   del splitted[0]
   if splitted[0]=="":
      del splitted[0]
   del splitted[-1]
   if splitted[-1]=="":
      del splitted[-1]
   return len(splitted), splitted

@client.event
async def on_ready():
   print("> Bot connected")

@client.event
async def on_message(message):
   if(check_message(message.content)=="ranking"):
      await ranking(message)
   elif(check_message(message.content)=="sutom"):
      if not check_if_already_sent(str(message.author)):
         tentatives, splitted = process_message(message.content)
         msg_content="Data successfully saved !"
         if(tentatives==6 and splitted[-1]=='🟥🟥🟥🟥🟥🟥'):
            msg_content += " But you won't get any points !"
         else:
            msg_content += " You got " + str(get_points(tentatives)) + " points !"
         
         # save the info in the json file
         obj = {
            "date": datetime.now().strftime("%d/%m/%Y"),
            "pseudo": str(message.author),
            "tentatives": tentatives,
            "points": get_points(tentatives)
         }
         store_obj(obj)

         await message.channel.send(embed=create_embed(msg_content))
      else:
         await message.channel.send(embed=create_embed("You already sent your results ! Dont try to cheat !"))

async def ranking(message):
   with open(filename, "r") as f:
      stored = json.load(f)
   stored.sort(key=lambda x: x["points"], reverse=True)
   msg = "```\n"
   msg += "Daily Ranking\n"
   msg += "-------\n"
   for i in range(len(stored)):
      msg += str(i+1) + " - " + stored[i]["pseudo"] + " : " + str(stored[i]["points"]) + "\n"
   msg += "```"
   await message.channel.send(embed=create_embed(msg))

client.run(TOKEN)
