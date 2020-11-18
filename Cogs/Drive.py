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
            
            for file in message.attachments:
                fName = '.'.join(file.filename.split('.')[:-1])
                fExtension = file.filename.split('.')[-1]
                fileDupCount = 0
                fileName = file.filename
                
                while True:
                    if not os.path.exists(f'{driveDir}/{fileName}'):
                        r = requests.get(file.url, allow_redirects=True)
                        with open(f'{driveDir}/{fileName}', 'wb') as f:
                            f.write(r.content)
                            
                        # Save Data
                        dataDict1 = { fileName: { 'originalName': file.filename, 'url': file.url } }
                        dataDict2 = { fileName: { 'originalName': file.filename, 'path': f'{driveDir}/{fileName}', 'url': file.url } }
                        
                        fDataPath = f'{drivePath}/{DRIVE_FILE_ALL_DATA}'
                        if not os.path.exists(fDataPath):
                            with open(fDataPath, 'w', -1, 'utf-8') as f:
                                json.dump(dataDict2, f, indent=4, sort_keys=True)
                        else:
                            with open(fDataPath, 'r+', -1, 'utf-8') as f:
                                data = json.load(f)
                                data.update(dataDict2)
                                f.seek(0)
                                json.dump(data, f, indent=4, sort_keys=True)
                        
                        fDataPath = f'{driveDir}/{DRIVE_FILE_DATA}'
                        if not os.path.exists(fDataPath):
                            with open(fDataPath, 'w', -1, 'utf-8') as f:
                                json.dump(dataDict1, f, indent=4, sort_keys=True)
                        else:
                            with open(fDataPath, 'r+', -1, 'utf-8') as f:
                                data = json.load(f)
                                data.update(dataDict1)
                                f.seek(0)
                                json.dump(data, f, indent=4, sort_keys=True)
                            
                        break
                    else:
                        fileDupCount += 1
                        fileName = f'{fName}{fileDupCount}.{fExtension}'
                        

def setup(bot):
    bot.add_cog(Drive(bot))
