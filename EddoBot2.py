import discord
import os
import random
from time import sleep
from datetime import datetime
import TwitterBot as tw
import EddoBotUtil as ed

from discord import raw_models

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}. CURRENTLY UNDER DEVELOPMENT OF EDDOBOT2'.format(client))

@client.event
async def on_message(message):
    msgauth = str(message.author).split("#")[0]
    print(msgauth + ": " + message.content)

    if message.author == client.user:
        return

    bot_response = ed.bot_respond(message)
    if(bot_response is not None): #Generic EddoBot response for keywords
        await message.channel.send(bot_response)
    
    command_string = ed.handler(message)
    if(command_string is not None):
        await message.channel.send(command_string)

#ADD DISCORD CREDS HERE