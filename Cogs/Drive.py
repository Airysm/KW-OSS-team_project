# -*- coding: utf-8 -*-
# drive.py

import os
import json
import discord
from discord.ext import commands


DRIVE_PATH = 'Drive'
DRIVE_FILE_ALL_DATA = 'File_ALL_Data.json'
DRIVE_FILE_DATA = 'File_Data.json'



class Drive(commands.Cog, name='Drive'):
    def __init__(self, bot):
        self.bot = bot
        if not os.path.exists(DRIVE_PATH):
            os.mkdir(DRIVE_PATH)



def setup(bot):
    bot.add_cog(Drive(bot))
