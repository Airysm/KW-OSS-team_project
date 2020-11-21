# -*- coding: utf-8 -*-
# miniRPG.py

import discord
from discord.ext import commands
from time import sleep
import asyncio

class Skill():
    INT = 1
    MP = 1
    DEX = 1
    STR = 1

    def 공격(self):
        return self.INT * 3

    def 방어(self):
        return self.STR * 2
    
    def 방어(self):
        return self.DEF * 2

class Boss():
    def __init__(self):
        self.HP = 20
        self.MP = 10
        self.DEF = 2
        self.STR = 7
        self.INT = 5
        self.DEX = 1

    def reset(self):
        self.HP = 20
        self.MP = 10
        self.DEF = 2
        self.ATK = 7
        self.INT = 5
        self.DEX = 1

class Hero(Skill):
    def __init__(self):
        self.HP = 10
        self.MP = 10
        self.DEF = 1
        self.STR = 5
        self.INT = 5
        self.DEX = 1

    def reset(self):
        self.HP = 10
        self.MP = 10
        self.DEF = 1
        self.STR = 5
        self.INT = 5
        self.DEX = 1

man = Hero()
dragon = Boss()

class MiniRPG(commands.Cog, name='MiniRPG'):
    game_set = 0

    @commands.Cog.listener('on_message')
    async def my_message(self, message):
        if message.author == self.bot.user:
            return

        print('two')
    
    @commands.command(name='RPG')
    async def Game_init(self, ctx):
        await ctx.send('시작됩니다.')
        game_set = 1

        man.reset()
        dragon.reset()

        embed = discord.Embed(title='원하는 스킬을 선택하세요', description='?', color=0x147AF3)
        message = await ctx.send(embed=embed)

        while man.HP > 0 and dragon.HP > 0:
            sleep(1)
            
            msg = await ctx.bot.wait_for('message')
            if ctx.author == msg.author:
                await message.edit(content='선택하셨습니다!')
            self.Boss_Turn(dragon)
            await ctx.send(str(dragon.HP) + ' 로 증가되었습니다.')
        
        game_set = 0

    @commands.command(name='skills')
    async def skill_info(self, ctx):
        embed = discord.Embed(title='Skill', description='1. Electric')
        await ctx.send(embed = embed)

    @commands.command(name='MyHP')
    async def check_HP(self, ctx, Hero = man):
        if game_set == 1:
            embed = discord.Embed(description = Hero.HP)
            await ctx.send(embed = embed)
        else:
            await ctx.send('게임이 시작하지 않았습니다.')
        
    def My_Turn(self, hero):
        hero.HP = hero.HP + 1
    
    def Boss_Turn(self, boss):
        boss.HP = boss.HP - 2

    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(MiniRPG(bot))