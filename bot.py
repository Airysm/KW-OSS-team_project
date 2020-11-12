# -*- coding: utf-8 -*-
# bot.py

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


bot = commands.Bot(command_prefix='!!')


bot.remove_command('help')

for filename in os.listdir('Cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'Cogs.{filename[:-3]}')
        

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name='( ͡° ͜ʖ ͡°)'))
        

    
    
    
    
#####
@bot.command(name='로드')
async def load_commands(ctx, extension):
    await ctx.message.delete()
    bot.load_extension(f'Cogs.{extension}')
    m = await ctx.send(f':white_check_mark: {extension} loaded!')
    await asyncio.sleep(0.5)
    await m.delete()
    
@bot.command(name='언로드')
async def unload_commands(ctx, extension):
    await ctx.message.delete()
    bot.unload_extension(f'Cogs.{extension}')
    m = await ctx.send(f':white_check_mark: {extension} unloaded!')
    await asyncio.sleep(0.5)
    await m.delete()

@bot.command(name='리로드')
async def reload_commands(ctx, extension=None):
    await ctx.message.delete()
    if extension is None:
        for filename in os.listdir('Cogs'):
            if filename.endswith('.py'):
                bot.unload_extension(f'Cogs.{filename[:-3]}')
                bot.load_extension(f'Cogs.{filename[:-3]}')
                m = await ctx.send(':white_check_mark: All Command reloaded!')
                await asyncio.sleep(0.5)
                await m.delete()
    else:
        bot.unload_extension(f'Cogs.{extension}')
        bot.load_extension(f'Cogs.{extension}')
        m = await ctx.send(f':white_check_mark: {extension} reloaded!')
        await asyncio.sleep(0.5)
        await m.delete()
#####



bot.run(TOKEN)
