# -*- coding: utf-8 -*-
# drive.py

import os
import datetime
import json
import discord
from discord.ext import commands


DATA_PATH = 'Data'
DRIVE_PATH = 'Drive'
DRIVE_FILE_ALL_DATA = 'File_ALL_Data.json'
DRIVE_FILE_DATA = 'File_Data.json'



class Drive(commands.Cog, name='Drive'):
    def __init__(self, bot):
        self.bot = bot
        if not os.path.exists(DATA_PATH):
            os.mkdir(DATA_PATH)


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.attachments:
            guildPath = f'{DATA_PATH}/{message.guild.id}'
            if not os.path.exists(guildPath):
                os.mkdir(guildPath)
                f = open(f'{guildPath}/_{message.guild.name}', 'w')
                f.close()
                
            drivePath = f'{guildPath}/{DRIVE_PATH}'
            if not os.path.exists(drivePath):
                os.mkdir(drivePath)
            
            dTime = datetime.datetime.today()
            curDate = dTime.strftime('%Y%m%d')
            driveDir = f'{drivePath}/Drive_{curDate}'
            if not os.path.exists(driveDir):
                os.mkdir(driveDir)
            

def setup(bot):
    bot.add_cog(Drive(bot))
