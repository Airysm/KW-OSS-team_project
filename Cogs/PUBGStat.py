# -*- coding: utf-8 -*-
# pubgstat.py

import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests


koreanParam = '?hl=ko-KR'
bgstatURL = 'https://dak.gg/'
bgstatUserURL = 'https://dak.gg/profile/'
platformList = ['스팀', '카카오']
no_record = 'no_record'
rankSize = 4
FPP_Text = '(FPP)'

        
class PUBGStat(commands.Cog, name='PUBGStat'):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='배그')
    async def pubg(self, ctx, userName, mode='tpp'):
        html = requests.get(bgstatUserURL + userName + koreanParam).text
        bs = BeautifulSoup(html, 'html.parser')
        
        if(not bs.select('.not_found')):
            
            isStatFind = False
            
            platformIndex = 0
            if not platformList[0] in bs.select('.regions')[0].text.strip():
                platformIndex = 1
            
            
            
            playerName = bs.select('.nick')[0].get('data-nick')
            playerIconUrl = bs.select('.userInfo > img')[0].get('src')
            if platformIndex == 1:
                playerIconUrl = bgstatURL + playerIconUrl
            
            embed = discord.Embed(title=f'{playerName} - {platformList[platformIndex]}', url=f'{bgstatUserURL}{playerName}/', color=0xFF0000)
            
            #rankList = bs.select('.ranked')
            rankList = bs.select('.modeItem')
            rangeStart = 0
            if mode == 'fpp':
                rangeStart = 2
                
            for index, r in enumerate(rankList[rangeStart:]):
                if index < rankSize:
                    # Rank
                    if no_record not in r.get('class'):
                        
                        tier = r.select('.rating > span')[0].text.strip()
                        ratingPoint = r.select('.rating > span')[1].text.strip()
                        rating = r.select('.win-stats')[0].text.strip()
                        embed.add_field(name=f'{tier} - {ratingPoint}', value=rating, inline=False)
                        
                        mode = r.select('h1')[0].text.strip()
                        mode = mode[:-len(rating)].strip()
                        if FPP_Text in mode:
                            mode = mode[:-len(FPP_Text)].strip() + f' {FPP_Text}'
                        embed.description = mode
                        
                        statList = r.select('.stats-item')
                        
                        for i in range(len(statList)):
                            label = statList[i].select('label')[0].text.strip()
                            value = statList[i].select('p')[0].text.strip()
                            if value[-1] == '%':
                                value = value[:-1].strip() + ' %'
                            embed.add_field(name=label, value=value)
                        
                        isStatFind = True
                        break
                else:
                    #Casual
                    casualList = r.select('.mode-section')
                    if mode == 'fpp':
                        rangeStart = 1
                    for c in casualList[rangeStart::rangeStart+1]:
                        if no_record not in c.get('class'):
                            
                            tier = c.select('.rating > span')[0].text.strip()
                            ratingPoint = c.select('.rating > span')[1].text.strip()
                            rating = c.select('.win-stats')[0].text.strip()
                            embed.add_field(name=f'{tier} - {ratingPoint}', value=rating, inline=False)
                            
                            mode = c.select('h1')[0].text.strip()
                            mode = mode[:-len(rating)].strip()
                            if FPP_Text in mode:
                                mode = mode[:-len(FPP_Text)].strip() + f' {FPP_Text}'
                            playTime = c.select('.time_played')
                            if playTime:
                                playTime = playTime[0].text.strip()
                                mode = mode[:-len(playTime)].strip()
                            embed.description = mode
                            
                            statList = c.select('.stats-item')
                            
                            for i in range(len(statList)):
                                label = statList[i].select('label')[0].text.strip()
                                value = statList[i].select('p')[0].text.strip()
                                if value[-1] == '%':
                                    value = value[:-1].strip() + ' %'
                                embed.add_field(name=label, value=value)
                            
                            isStatFind = True
                            break
                    if isStatFind == True:
                        break
                          
            if isStatFind == False:
                embed.description = '플레이 기록이 없습니다'
                
            embed.set_thumbnail(url=playerIconUrl)
            await ctx.send(content='배그 전적', embed=embed)
        else:
            await ctx.send('플레이어가 존재하지 않습니다.')
        
        


def setup(bot):
    bot.add_cog(PUBGStat(bot))
