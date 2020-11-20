# -*- coding: utf-8 -*-
# log.py

import os
import datetime
import discord
from discord.ext import commands

DATA_PATH = 'Data'
LOG_PATH = 'Logs'
MESSAGE_MODE = ['메시지', '수정', '삭제']

class Log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if not os.path.exists(DATA_PATH):
            os.mkdir(DATA_PATH)
        
            
        
    @commands.Cog.listener()
    async def on_message(self, message):
        guildPath = f'{DATA_PATH}/{message.guild.id}'
        if not os.path.exists(guildPath):
            os.mkdir(guildPath)
            f = open(f'{guildPath}/_{message.guild.name}', 'w')
            f.close()
            
        logPath = f'{guildPath}/{LOG_PATH}'
        if not os.path.exists(logPath):
            os.mkdir(logPath)
            
        logPath += f'/{message.channel.id}'
        if not os.path.exists(logPath):
            os.mkdir(logPath)
            f = open(f'{logPath}/_{message.channel.name}', 'w')
            f.close()
            
        
        dTime = datetime.datetime.today()
        curDate = dTime.strftime('%Y%m%d')
        curTime = dTime.strftime('%X:%f')
        logFileName = f'Log_{curDate}.log'
        with open(f'{logPath}/{logFileName}', 'a+', -1, 'utf-8') as f:
            f.write(f'[{curTime}] [{message.channel.name}] [{MESSAGE_MODE[0]}] [{message.author.nick}-{message.author}-{message.author.id}] [{message.id}] {message.content}\n')
            if message.attachments:
                f.write(f'attachment - {message.attachments}\n')
            if message.embeds:
                f.write(f'embed - {message.embeds[0].to_dict()}\n')
                
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        guildPath = f'{DATA_PATH}/{message.guild.id}'
        if not os.path.exists(guildPath):
            os.mkdir(guildPath)
            f = open(f'{guildPath}/_{message.guild.name}', 'w')
            f.close()
            
        logPath = f'{guildPath}/{LOG_PATH}'
        if not os.path.exists(logPath):
            os.mkdir(logPath)
            
        logPath += f'/{message.channel.id}'
        if not os.path.exists(logPath):
            os.mkdir(logPath)
            f = open(f'{logPath}/_{message.channel.name}', 'w')
            f.close()
            
        
        dTime = datetime.datetime.today()
        curDate = dTime.strftime('%Y%m%d')
        curTime = dTime.strftime('%X:%f')
        logFileName = f'Log_{curDate}.log'
        with open(f'{logPath}/{logFileName}', 'a+', -1, 'utf-8') as f:
            if type(message.author) is discord.user.User:
                f.write(f'[{curTime}] [{message.channel.name}] [{MESSAGE_MODE[2]}] [{message.author}-{message.author.id}] [{message.id}] {message.content}\n')
            else:
                f.write(f'[{curTime}] [{message.channel.name}] [{MESSAGE_MODE[2]}] [{message.author.nick}-{message.author}-{message.author.id}] [{message.id}] {message.content}\n')
            
        
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        guildPath = f'{DATA_PATH}/{before.guild.id}'
        if not os.path.exists(guildPath):
            os.mkdir(guildPath)
            f = open(f'{guildPath}/_{before.guild.name}', 'w')
            f.close()
            
        logPath = f'{guildPath}/{LOG_PATH}'
        if not os.path.exists(logPath):
            os.mkdir(logPath)
            
        logPath += f'/{before.channel.id}'
        if not os.path.exists(logPath):
            os.mkdir(logPath)
            f = open(f'{logPath}/_{before.channel.name}', 'w')
            f.close()
            
        
        dTime = datetime.datetime.today()
        curDate = dTime.strftime('%Y%m%d')
        curTime = dTime.strftime('%X:%f')
        logFileName = f'Log_{curDate}.log'
        with open(f'{logPath}/{logFileName}', 'a+', -1, 'utf-8') as f:
            if type(before.author) is discord.user.User:
                f.write(f'[{curTime}] [{before.channel.name}] [{MESSAGE_MODE[1]}] [{before.author}-{before.author.id}] [{before.id}] {before.content}\n')
            else:
                f.write(f'[{curTime}] [{before.channel.name}] [{MESSAGE_MODE[1]}] [{before.author.nick}-{before.author}-{before.author.id}] [{before.id}] {before.content}\n')
            f.write(f'-> {after.content}\n')
        
    
    
def setup(bot):
    bot.add_cog(Log(bot))
