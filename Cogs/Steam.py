# -*- coding: utf-8 -*-
# steam.py

import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
import asyncio


koreanParam='?l=koreana'
#userFindURL='https://steamcommunity.com/search/users/#text='
userFindURL='https://steamcommunity.com/id/'
userFindURL_ID='https://steamcommunity.com/profiles/'
gameFindURL=f'https://store.steampowered.com/search/{koreanParam}&term='

numberEmoji = [ '0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟' ]
        
class Steam(commands.Cog, name='Steam'):
    gameSearchSize = 5
    gameSearchSizeMax = 10
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='스팀유저')
    async def suser(self, ctx, userName):
        userURL = ''
        if len(userName) == 17 and userName.isdigit():
            userURL = userFindURL_ID + userName + koreanParam
        else:
            userURL = userFindURL + userName + koreanParam
        html = requests.get(userURL).text
        userbs = BeautifulSoup(html, 'html.parser')
        
        if userbs.select('.profile_page'):
            realUserName = userbs.select('.actual_persona_name')[0].text
            userIconURL = userbs.select('.playerAvatarAutoSizeInner > img')[0].get('src')
            
            userMinInfoStr = ''
            isUserPrivate = True
            if not userbs.select('.profile_private_info'):
                isUserPrivate = False
                userMinInfo = userbs.select('.header_real_name > bdi')[0].text.strip()
                userCountry = userbs.select('.header_real_name')[0].text[len(userMinInfo)+1:].strip()
                userLevel = userbs.select('.friendPlayerLevelNum')[0].text
                userStatus = userbs.select('.profile_in_game_header')[0].text
            
                userMinInfoStr = userMinInfo
                if userCountry:
                    userMinInfoStr += f', {userCountry}'
            embed = discord.Embed(title=f'{realUserName}', description=userMinInfoStr, url=userURL, color=0x171a21)
            
            if not isUserPrivate:
                embed.add_field(name='Level', value=userLevel, inline=False)
                embed.add_field(name='Current Status', value=userStatus, inline=False)

            embed.set_thumbnail(url=userIconURL)
            
            await ctx.send(embed=embed)
        else:
            await ctx.send('플레이어가 존재하지 않습니다.')
        
        
    @commands.command(name='게임')
    async def sgame(self, ctx, *, gameName):
        html = requests.get(gameFindURL + gameName).text
        bs = BeautifulSoup(html, 'html.parser')
        
        titles = bs.select('.title')
        indexList = []
        index = 0
        for i in range(len(titles)):
            if titles[i].text.lower().find(gameName.lower()) >= 0:
                indexList.append(i)
        if len(indexList) == 1:
            index = indexList[0]
        elif len(indexList) > 1:
            for i in indexList:
                if titles[i].text.lower() == gameName.lower():
                    index = i
        
        result = bs.select('#search_resultsRows > a')
        if result:
            gameURL = result[index].get('href')
            gameURL = '/'.join(gameURL.split('/')[:-1]) + koreanParam
            
            gameImgURL = result[index].select('.search_capsule > img')[0].get('src')
            gameTitle = result[index].select('.title')[0].text
            gameReleased = result[index].select('.search_released')[0].text
            gameReview = result[index].select('.search_review_summary')
            if gameReview:
                gameReview = gameReview[0].get('data-tooltip-html').replace('<br>','\n')
            else:
                gameReview = ''
            gameDiscount = result[index].select('.search_discount')[0].text.strip()
            gamePrice = result[index].select('.search_price')[0].text.strip()
            gameDiscountPrice = result[index].select('.search_price strike')
            if gameDiscountPrice:
                gameDiscountPrice = gameDiscountPrice[0].text.strip()
                gamePrice = f'~~{gameDiscountPrice}~~\n-> {gamePrice[len(gameDiscountPrice):]}'
                
                
            embed = discord.Embed(title=f'{gameTitle}', description=gameReleased, url=gameURL, color=0x171a21)
            if gamePrice:
                embed.add_field(name='가격', value=gamePrice)
            if gameDiscount:
                embed.add_field(name='할인', value=gameDiscount)
            if gameReview:
                embed.add_field(name='리뷰', value=gameReview, inline=False)
            embed.set_thumbnail(url=gameImgURL)
            await ctx.send(embed=embed)
        else:
            await ctx.send('게임이 존재하지 않습니다.')
            
    
    @commands.command(name='게임검색')
    async def sgsearch(self, ctx, *, gameName):
        html = requests.get(gameFindURL + gameName).text
        bs = BeautifulSoup(html, 'html.parser')
        
        titles = bs.select('.title')
        titleSize = len(titles)
        if titleSize == 0:
            await ctx.send('게임이 존재하지 않습니다.')
            return
        
        if titleSize > self.gameSearchSize:
            titleSize = self.gameSearchSize + 1
        titleStr = '0. 취소\n'
        for i, t in enumerate(titles[:titleSize]):
            titleStr += f'{i+1}. {t.text}\n'
        embed_gameList = discord.Embed(title='원하는 게임을 선택하세요', description=titleStr, color=0x171a21)
        message = await ctx.send(embed=embed_gameList)
        
        for i in range(titleSize):
            await message.add_reaction(numberEmoji[i])
            
        selectIndex = 0
        while True:
            try:
                reaction, user = await ctx.bot.wait_for('reaction_add', timeout=60.0)
            except asyncio.TimeoutError:
                await message.edit(content='시간 초과!!')
                await message.clear_reactions()
                return
            else:
                if user == ctx.author and reaction.emoji in numberEmoji[:titleSize]:
                    selectIndex = numberEmoji[:titleSize].index(reaction.emoji)
                    break
                elif not user == self.bot.user:
                    await reaction.remove(user)
        
        await message.clear_reactions()
        
        result = bs.select('#search_resultsRows > a')[selectIndex]
        
        gameURL = result.get('href')
        gameURL = '/'.join(gameURL.split('/')[:-1]) + koreanParam
        
        gameImgURL = result.select('.search_capsule > img')[0].get('src')
        gameTitle = result.select('.title')[0].text
        gameReleased = result.select('.search_released')[0].text
        gameReview = result.select('.search_review_summary')
        if gameReview:
            gameReview = gameReview[0].get('data-tooltip-html').replace('<br>','\n')
        else:
            gameReview = ''
        gameDiscount = result.select('.search_discount')[0].text.strip()
        gamePrice = result.select('.search_price')[0].text.strip()
        gameDiscountPrice = result.select('.search_price strike')
        if gameDiscountPrice:
            gameDiscountPrice = gameDiscountPrice[0].text.strip()
            gamePrice = f'~~{gameDiscountPrice}~~\n-> {gamePrice[len(gameDiscountPrice):]}'
            
            
        embed = discord.Embed(title=f'{gameTitle}', description=gameReleased, url=gameURL, color=0x171a21)
        if gamePrice:
            embed.add_field(name='가격', value=gamePrice)
        if gameDiscount:
            embed.add_field(name='할인', value=gameDiscount)
        if gameReview:
            embed.add_field(name='리뷰', value=gameReview, inline=False)
        embed.set_thumbnail(url=gameImgURL)
        await message.edit(embed=embed)


    @commands.command(name='게임검색크기')
    async def sgsetsearchsize(self, ctx, searchSize: int):
        if searchSize > 0 and searchSize <= 10:
            self.gameSearchSize = searchSize
        elif searchSize > 10:
            self.gameSearchSize = 10
        else:
            await ctx.send('올바른 값을 입력해주세요!!')
            return
        await ctx.send(f'게임 검색 크기가 {self.gameSearchSize}로 변경되었습니다.')
            
        

def setup(bot):
    bot.add_cog(Steam(bot))
