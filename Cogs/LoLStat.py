# -*- coding: utf-8 -*-
# lolstat.py

import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests


lolstatUserURL = 'https://www.op.gg/summoner/userName='
no_data = 'unranked'

        
class LoLStat(commands.Cog, name='LoLStat'):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='롤')
    async def lol(self, ctx, *, userName):
        html = requests.get(lolstatUserURL + userName).text
        bs = BeautifulSoup(html, 'html.parser')
        
        if not bs.select('.Information > span'):
            await ctx.send('플레이어가 존재하지 않습니다.')
            
        level = bs.select('.ProfileIcon > span')[0].text
        playerName = bs.select('.Information > span')[0].text
        #iconURL = bs.select('.ProfileIcon > img')[0].get('src')
        
        statURLName = '+'.join(playerName.split(' '))
        embed = discord.Embed(title=f'{playerName} - Lv.{level}', url=f'{lolstatUserURL}{statURLName}', color=0xC2902C)
        
        if bs.select('.SummonerRatingMedium'):
            rank = bs.select('.SummonerRatingMedium')[0]
            if no_data not in rank.select('.TierRank')[0].get('class'):
                
                tierIconURL = rank.select('.Medal > img')[0].get('src')
                if not tierIconURL.startswith('http'):
                    tierIconURL = f'https:{tierIconURL}'
                
                rankType = rank.select('.RankType')[0].text
                tierRank = rank.select('.TierRank')[0].text
                LP = rank.select('.LeaguePoints')[0].text.strip()
                win = rank.select('.wins')[0].text
                lose = rank.select('.losses')[0].text
                ratio = rank.select('.winratio')[0].text
                leagueName = rank.select('.LeagueName')[0].text.strip()
                
                
                if bs.select('.Information > .Team'):
                    team = bs.select('.Information > .Team')[0].text.strip()
                    teamName = bs.select('.Information > .Team > .Name')[0].text.strip()
                    team = team[:-len(teamName)].strip()
                    embed.description = f'{team} {teamName}'
                    
                    
                if bs.select('.LadderRank'):
                    ladderRank = bs.select('.LadderRank > a')[0].text.strip()
                    embed.add_field(name=rankType, value=ladderRank, inline=False)
                else:
                    embed.add_field(name=rankType, value=leagueName, inline=False)
                
            
                embed.add_field(name=tierRank, value=LP, inline=False)
                embed.add_field(name=f'{win} / {lose}', value=ratio, inline=False)
                
                embed.set_thumbnail(url=tierIconURL)
                
                await ctx.send(content='롤 전적', embed=embed)
                return
        
        embed.description = '기록된 전적이 없습니다.'
        await ctx.send(content='롤 전적', embed=embed)
        
        


def setup(bot):
    bot.add_cog(LoLStat(bot))
