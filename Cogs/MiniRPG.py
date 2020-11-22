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
    DEF = 1

    def 공격(self):
        return self.STR * 1

    def 방어(self):
        return self.DEF * 1
    
    def 힐(self):
        return self.INT * 2

class Boss(Skill):
    def __init__(self):
        self.HP = 100
        self.MP = 10
        self.DEF = 2
        self.STR = 5
        self.INT = 5
        self.DEX = 1

    def reset(self):
        self.HP = 100
        self.MP = 10
        self.DEF = 2
        self.ATK = 5
        self.INT = 5
        self.DEX = 1

class Hero(Skill):
    def __init__(self):
        self.HP = 100
        self.MP = 10
        self.DEF = 1
        self.STR = 5
        self.INT = 5
        self.DEX = 1

    def reset(self):
        self.HP = 100
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
        sleep(1)
        game_set = 1
        turn = 1

        man.reset()
        dragon.reset()

        #embed = discord.Embed(title='원하는 스킬을 선택하세요', description='?', color=0x147AF3)
        #message = await ctx.send(embed=embed)
        await ctx.send("\"1번째 당신의 턴\"")
        sleep(1)

        embed = discord.Embed(title='MiniRPG 실행어')
        embed.add_field(name='공격', value='\n'.join(['STR * 1']), inline=True)
        embed.add_field(name='힐', value='\n'.join(['INT * 2']), inline=True)
        embed.add_field(name='방어', value='\n'.join(['DEF * 1']), inline=True)
        await ctx.send(embed=embed)
        sleep(1)

        while man.HP > 0 and dragon.HP > 0:
            check = 0
            msg = await ctx.bot.wait_for('message')
            if ctx.author == msg.author:
                if(msg.content.startswith('!!')):
                    continue
                elif(msg.content == '힐'):
                    await ctx.send('당신은 자신의 체력을 회복했습니다.')
                    Heal = 0
                    if(man.HP + man.힐() > 100):
                        Heal = 100 - man.HP
                        man.HP = 100
                    else:
                        man.HP = man.HP + man.힐()
                        Heal = man.힐()
                    await ctx.send('자신의 체력이 ' + str(Heal) + '만큼 올랐습니다.')
                    sleep(1)
                    check = 1
                elif(msg.content == '공격'):
                    await ctx.send('당신은 보스를 공격했습니다.')
                    dragon.HP = dragon.HP - man.공격()
                    await ctx.send('보스의 체력이 ' + str(man.공격()) + '만큼 줄어 ' + str(dragon.HP) + '가 되었습니다.')
                    sleep(1)
                    check = 1
                else:
                    await ctx.send('제대로 된 행동을 하지 못했습니다!')
            if(self.my_turn_check(check)):
                await ctx.send('\"' + str(turn) + '번째 보스의 턴\"')
                sleep(1)
                turn = turn + 1
                boss_act = self.Boss_Turn(dragon)
                if(boss_act == 1):
                    await ctx.send('보스가 당신을 공격했습니다! 당신의 체력: ' + str(man.HP))
                    sleep(1)
                elif(boss_act == 2):
                    await ctx.send('보스가 자신의 체력을 회복했습니다. 보스의 체력: ' + str(dragon.HP))
                    sleep(1)
                await ctx.send('\"' + str(turn) + '번째 당신의 턴\"')

        if(man.HP <= 0):
            await ctx.send('당신은 쓰러졌습니다.. 패배.')
        else:
            await ctx.send('보스를 쓰러트렸습니다! 성공.')
        
        game_set = 0

    @commands.command(name='RPG스킬')
    async def skill_info(self, ctx):
        embed = discord.Embed(title='MiniRPG 실행어')
        embed.add_field(name='공격', value='\n'.join(['STR * 1']), inline=True)
        embed.add_field(name='힐', value='\n'.join(['INT * 2']), inline=True)
        embed.add_field(name='방어', value='\n'.join(['DEF * 1']), inline=True)
        await ctx.send(embed=embed)
    
    def Boss_Turn(self, boss):
        if(boss.HP >= 20):
            man.HP = man.HP - boss.공격()
            if(man.HP < 0):
                man.HP = 0
            return 1
        elif(boss.HP < 20):
            boss.HP = boss.HP + boss.힐()
            if(boss.HP > 100):
                boss.HP = 100
            return 2
    def my_turn_check(self, check):
        if(check == 0):
            return False
        else:
            return True

    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(MiniRPG(bot))