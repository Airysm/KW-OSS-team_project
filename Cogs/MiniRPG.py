# -*- coding: utf-8 -*-
# miniRPG.py

import discord
from discord.ext import commands
from time import sleep
import asyncio
import random


class Skill():
    INT = 1
    MP = 1
    DEX = 1
    STR = 1
    DEF = 1
    cooltime1 = 0
    cooltime2 = 0
    shock = False

    def 공격(self):
        return self.STR * 1

    def 힐(self):
        return self.INT * 2

    def 스킬(self):  # 쿨타임 3턴
        if (self.cooltime1 == 0):
            self.cooltime1 = 3
            return self.INT * 3
        else:
            return 0

    def 전격(self, boss):
        if (self.cooltime2 == 0):
            self.cooltime2 = 5
            boss.shock = True
            return 1
        else:
            return 0


class Boss(Skill):
    def __init__(self):
        self.HP = 100
        self.DEF = 1
        self.STR = 5
        self.INT = 5

    def reset(self):
        self.HP = 100
        self.DEF = 1
        self.ATK = 5
        self.INT = 5


class Hero(Skill):
    def __init__(self):
        self.HP = 100
        self.DEF = 1
        self.STR = random.randint(1, 9)
        self.INT = 10 - self.STR

    def reset(self):
        self.HP = 100
        self.DEF = 1
        self.STR = random.randint(1, 9)
        self.INT = 10 - self.STR


man = Hero()
dragon = Boss()


class MiniRPG(commands.Cog, name='MiniRPG'):

    @commands.command(name='RPG')
    async def Game_init(self, ctx):
        await ctx.send('시작됩니다.')
        sleep(1)
        game_set = 1
        turn = 1

        man.reset()
        dragon.reset()

        # embed = discord.Embed(title='원하는 스킬을 선택하세요', description='?', color=0x147AF3)
        # message = await ctx.send(embed=embed)
        await ctx.send('스탯이 랜덤하게 결정됩니다.')
        sleep(1)
        embed = discord.Embed(title='유저 스탯')
        embed.add_field(name='STR', value='\n'.join([str(man.STR)]), inline=True)
        embed.add_field(name='INT', value='\n'.join([str(man.INT)]), inline=True)
        await ctx.send(embed=embed)
        sleep(1)

        embed = discord.Embed(description='\"1번째 당신의 턴\"')
        await ctx.send(embed=embed)

        embed = discord.Embed(title='MiniRPG 실행어')
        embed.add_field(name='공격', value='\n'.join(['STR * 1']), inline=True)
        embed.add_field(name='힐', value='\n'.join(['INT * 2']), inline=True)
        embed.add_field(name='스킬', value='\n'.join(['INT * 3 \n쿨타임 3초']), inline=True)
        embed.add_field(name='전격', value='\n'.join(['1턴 행동불가']), inline=True)
        await ctx.send(embed=embed)
        sleep(1)

        while man.HP > 0 and dragon.HP > 0:
            check = 0
            if (man.shock == True):  # 보스가 전격 스킬을 썼을 때
                embed = discord.Embed(description='당신은 마비에 걸려있습니다!')
                await ctx.send(embed=embed)
                sleep(1)
                check = 1  # 턴이 지나감
                man.shock = False  # 마비 풀림
            else:
                msg = await ctx.bot.wait_for('message')
                if (ctx.author == msg.author and ctx.channel == msg.channel):  # 명령어의 사용자의 메세지만 취급
                    if (msg.content.startswith('!!')):  # 다른 명령어를 받을 경우 패스
                        continue
                    elif (msg.content == '힐'):  # 자신에게 힐
                        embed = discord.Embed(description='당신은 자신의 체력을 회복했습니다.')
                        await ctx.send(embed=embed)
                        sleep(1)
                        Heal = 0
                        if (man.HP + man.힐() > 100):  # 최대체력이 100 이므로 안 넘어가게 체크
                            Heal = 100 - man.HP
                            man.HP = 100
                        else:
                            man.HP = man.HP + man.힐()
                            Heal = man.힐()
                        embed = discord.Embed(description='자신의 체력이 ' + str(Heal) + ' 만큼 올랐습니다.')
                        await ctx.send(embed=embed)
                        sleep(1)
                        check = 1  # 자신의 턴을 무사히 완료
                    elif (msg.content == '공격'):  # 보스에게 공격
                        embed = discord.Embed(description='당신은 보스를 공격했습니다.')
                        await ctx.send(embed=embed)
                        dragon.HP = dragon.HP - man.공격()
                        embed = discord.Embed(
                            description='보스의 체력이 ' + str(man.공격()) + '만큼 줄어 ' + str(dragon.HP) + '가 되었습니다.')
                        await ctx.send(embed=embed)
                        sleep(1)
                        check = 1  # 자신의 턴을 무사히 완료
                    elif (msg.content == '스킬'):  # 보스에게 스킬 사용
                        skill_check = man.스킬()  # 상황에 따른 값 반환
                        if (skill_check == 0):  # 스킬이 쿨타임 일 때
                            embed = discord.Embed(description='스킬의 쿨타임이 ' + str(man.cooltime1) + ' 만큼 남았습니다.')
                            await ctx.send(embed=embed)
                            sleep(1)
                        else:  # 스킬이 사용 가능할 때
                            dragon.HP = dragon.HP - skill_check
                            embed = discord.Embed(description='당신은 스킬을 사용하였습니다!')
                            await ctx.send(embed=embed)
                            sleep(1)
                            embed = discord.Embed(
                                description='보스의 체력이' + str(skill_check) + '만큼 줄어 ' + str(dragon.HP) + '가 되었습니다.')
                            await ctx.send(embed=embed)
                            sleep(1)
                            check = 1  # 자신의 턴을 무사히 완료
                    elif (msg.content == '전격'):  # 보스에게 전격 사용
                        skill_check = man.전격(dragon)  # 상황에 따른 값 반환
                        if (skill_check == 0):  # 스킬이 쿨타임 일 때
                            embed = discord.Embed(description='스킬의 쿨타임이 ' + str(man.cooltime2) + ' 만큼 남았습니다.')
                            await ctx.send(embed=embed)
                            sleep(1)
                        else:  # 스킬이 사용 가능할 때
                            if (turn > 6):  # 드래곤이 브레스를 쏘고 있을 경우
                                embed = discord.Embed(description='브레스를 막을 수 없습니다!')
                                await ctx.send(embed=embed)
                                sleep(1)
                                dragon.shock = False
                            else:  # 브레스를 쏘고 있지 않을 경우
                                embed = discord.Embed(description='당신은 보스에게 전격을 사용하였습니다!')
                                await ctx.send(embed=embed)
                                sleep(1)
                                embed = discord.Embed(description='보스가 마비에 걸렸습니다!')
                                await ctx.send(embed=embed)
                                sleep(1)
                            check = 1  # 자신의 턴을 무사히 완료
                    else:
                        await ctx.send('제대로 된 행동을 하지 못했습니다!')
            # 자신의 턴이 제대로 완료 되었으면 보스의 턴 실행
            if (self.my_turn_check(check)):
                embed = discord.Embed(description='\"' + str(turn) + '번째 보스의 턴\"')
                await ctx.send(embed=embed)
                sleep(1)
                if (dragon.shock == True):  # 보스가 마비에 걸려있을 때
                    embed = discord.Embed(description='보스는 마비에 걸려있습니다!')
                    await ctx.send(embed=embed)
                    sleep(1)
                    dragon.shock = False
                elif (turn == 10):  # 10턴 까지 버틸 경우 유저 즉사
                    man.HP = 0
                    embed = discord.Embed(description='보스가 브레스를 발사했습니다!')
                    await ctx.send(embed=embed)
                    sleep(1)
                    embed = discord.Embed(description='당신은 브레스를 버티지 못했습니다...')
                    sleep(1)
                elif (turn >= 5):  # 6턴 이상일 때부터는 최종 패턴 돌입
                    embed = discord.Embed(description='보스가 브레스를 준비중입니다!')
                    await ctx.send(embed=embed)
                    sleep(1)
                else:
                    boss_act = self.Boss_Turn(dragon)  # 보스가 행동한 것에 따라 다른 리턴 값을 가짐
                    if (boss_act == 1):  # 보스가 공격했을 경우
                        embed = discord.Embed(description='보스가 당신을 공격했습니다! 당신의 체력: ' + str(man.HP))
                        await ctx.send(embed=embed)
                        sleep(1)
                    elif (boss_act == 2):  # 보스가 자신의 체력을 회복했을 경우
                        embed = discord.Embed(description='보스가 자신의 체력을 회복했습니다. 보스의 체력: ' + str(dragon.HP))
                        await ctx.send(embed=embed)
                        sleep(1)
                    elif (boss_act == 3):  # 보스가 스킬을 사용한 경우
                        embed = discord.Embed(description='보스가 당신에게 스킬을 사용했습니다! 당신의 체력 ' + str(man.HP))
                        await ctx.send(embed=embed)
                        sleep(1)
                    elif (boss_act == 4):  # 보스가 전격을 사용한 경우
                        embed = discord.Embed(description='보스가 당신에게 전격을 사용했습니다!')
                        await ctx.send(embed=embed)
                        sleep(1)
                turn = turn + 1  # 턴 수 증가
                if (man.cooltime1 > 0):  # 쿨타임 턴수 감소
                    man.cooltime1 = man.cooltime1 - 1
                if (man.cooltime2 > 0):
                    man.cooltime2 = man.cooltime2 - 1
                if (dragon.cooltime1 > 0):
                    dragon.cooltime1 = dragon.cooltime1 - 1
                if (dragon.cooltime2 > 0):
                    dragon.cooltime2 = dragon.cooltime2 - 1
                if (man.HP <= 0 or dragon.HP < 0):
                    pass
                else:
                    embed = discord.Embed(description='\"' + str(turn) + '번째 당신의 턴\"')
                    await ctx.send(embed=embed)
                    sleep(1)

        if (man.HP <= 0):  # 유저의 HP 가 0 이하일 경우
            embed = discord.Embed(description='당신은 쓰러졌습니다.. 패배.')
            await ctx.send(embed=embed)
        else:  # 보스의 HP 가 0 이하일 경우
            embed = discord.Embed(description='보스를 쓰러트렸습니다! 성공!')
            await ctx.send(embed=embed)
        game_set = 0  # 게임이 끝남

    @commands.command(name='RPG설명')
    async def skill_info(self, ctx):
        embed = discord.Embed(description='보스와 한번씩 번갈아가며 행동을 취하는 턴제 미니게임입니다.')
        await ctx.send(embed=embed)
        embed = discord.Embed(title='MiniRPG 실행어')
        embed.add_field(name='공격', value='\n'.join(['STR * 1']), inline=True)
        embed.add_field(name='힐', value='\n'.join(['INT * 2']), inline=True)
        embed.add_field(name='스킬', value='\n'.join(['INT * 3\n쿨타임 3턴']), inline=True)
        embed.add_field(name='전격', value='\n'.join(['1턴 행동불가\n쿨타임 5턴']), inline=True)
        await ctx.send(embed=embed)
        embed = discord.Embed(description='자신의 턴에 위의 단어 중 1개를 적으면 행동을 취합니다.')
        await ctx.send(embed=embed)
        embed = discord.Embed(description='체력이 먼저 0이 되는 쪽이 패배합니다.')
        await ctx.send(embed=embed)

    # 보스가 자신의 턴에 행동해야 할 인공지능
    def Boss_Turn(self, boss):
        if (dragon.cooltime1 == 0):  # 스킬을 쓸 수 있으면
            man.HP = man.HP - dragon.스킬()
            if (man.HP < 0):  # 최소 체력이 0이므로 아래로 내려갈 경우
                man.HP = 0  # 0으로 변경
            return 3
        elif (dragon.cooltime2 == 0):  # 전격을 쓸 수 있으면
            dragon.전격(man)
            return 4
        elif (boss.HP >= 20):  # 체력이 20 이상이면
            man.HP = man.HP - boss.공격()  # 공격
            if (man.HP < 0):  # 최소 체력이 0이므로 아래로 내려갈 경우
                man.HP = 0  # 0으로 변경
            return 1
        elif (boss.HP < 20):  # 체력이 20 이하이면
            boss.HP = boss.HP + boss.힐()  # 힐
            if (boss.HP > 100):  # 최대 체력이 100이므로 위로 올라갈 경우
                boss.HP = 100  # 100으로 변경
            return 2

    # 숫자에 따른 True, False 를 return 하기 위한 함수
    def my_turn_check(self, check):
        if (check == 0):
            return False
        else:
            return True

    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(MiniRPG(bot))