# -*- coding: utf-8 -*-
# team.py

import discord
from discord.ext import commands
import random


class Team(commands.Cog):
    teamSize = 0;
    playerSize = 0;
    
    teamList = []
    teamJoinCount = 0
    teamMax = 0
    teamOverflowCount = 0
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='teamset', help='팀 세팅', usage='!!team 팀인원 플레이어수')
    async def team_setting(self, ctx, _teamSize: int, _playerSize: int):
        if _teamSize > _playerSize:
            await ctx.send('팀 인원보다 플레이어의 수가 더 많습니다!!')
        elif not (_teamSize > 0 and _playerSize > 0):
            await ctx.send('올바른 값을 입력해주세요!!')
        else:
            self.teamSize = _teamSize
            self.playerSize = _playerSize
            self.teamList = []
            self.teamJoinCount = 0
            self.teamMax = (self.playerSize) // self.teamSize
            self.teamOverflowCount = self.playerSize % self.teamSize
            
            embed = discord.Embed(title='팀이 세팅되었습니다')
            embed.add_field(name='팀 인원', value=self.teamSize)
            embed.add_field(name='플레이어 수', value=self.playerSize)
            await ctx.send(embed=embed)
        
    @commands.command(name='team', help='팀', usage='!!team')
    async def team(self, ctx):
        if self.teamSize == 0:
            await ctx.send('팀 세팅을 해주세요.')
        elif self.teamJoinCount == 0:
            await ctx.send('플레이어가 존재하지 않습니다.\n!!teamjoin 명령어를 사용해 팀에 들어가세요.')
        else:
            embed = discord.Embed(title='팀')
            embed.add_field(name='팀 인원', value=self.teamSize)
            embed.add_field(name='플레이어 수', value=self.playerSize)
        
            for i in range(len(self.teamList)):
                embed.add_field(name=f'팀 {i + 1}', value=', '.join(self.teamList[i]), inline=False)
        
            await ctx.send(embed=embed)
        
    @commands.command(name='teamjoin', help='팀 참가', usage='!!teamjoin')
    async def team_join(self, ctx):
        if self.teamSize ==  0:
            await ctx.send('팀 세팅을 해주세요.')
            return
        
        isPlayerExist = False
        playerTeamIndex = 0
        
        for i in range(len(self.teamList)):
            for player in self.teamList[i]:
                if player == ctx.author.name:
                    isPlayerExist = True
                    break
            if isPlayerExist:
                playerTeamIndex = i
                break
                
        if isPlayerExist:
            await ctx.send(f'이미 팀 {playerTeamIndex + 1}에 참가하셨습니다.')
        elif self.playerSize > self.teamJoinCount:
            while True:
                playerTeamIndex = random.randint(0, self.teamSize - 1)
                if len(self.teamList) <= playerTeamIndex:
                    playerTeamIndex = len(self.teamList)
                    self.teamList.append([ctx.author.name])
                    self.teamJoinCount += 1
                    break
                elif len(self.teamList[playerTeamIndex]) < self.teamMax:
                    self.teamList[playerTeamIndex].append(ctx.author.name)
                    self.teamJoinCount += 1
                    break
                elif self.teamOverflowCount > 0:
                    self.teamList[playerTeamIndex].append(ctx.author.name)
                    self.teamJoinCount += 1
                    self.teamOverflowCount -= 1
                    break
            await ctx.send(f'팀 {playerTeamIndex + 1}에 참가하셨습니다.')
        else:
            await ctx.send('팀이 꽉 찼습니다!!')
            
        


def setup(bot):
    bot.add_cog(Team(bot))
