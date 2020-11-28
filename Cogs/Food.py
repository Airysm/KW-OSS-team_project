#Food.py

import discord
from discord.ext import commands
from time import sleep
import asyncio
import random

korean_food=('부대찌개','보쌈','닭갈비','매운탕','돼지갈비','추어탕','회덮밥','물회','황태해장국','회','쭈꾸미','생선조림','김치전','호빵',
            '게장','순대국','김치찜','카레라이스','수제비','꼬치구이','꼬막정식','백숙','만두국','오므라이스','도시락','골뱅이소면','전',
            '어묵','김치찌개','떡꼬치','김치볶음밥','육회','뼈해장국','꼬막','콩나물국밥','돼지목살','제육덮밥','쌀밥','냉면','보리밥',
            '해물뚝배기','비빔메밀면','대게','오리고기','라면','생선구이','비빔국수','조개구이','콩국수','돼지국밥','닭발','순두부찌개'
            '떡튀순','한정식','불고기','칼국수','곱창','장어','뚝배기불고기','소머리국밥','양평해장국','설렁탕','길거리음식','감자탕',
            '떡볶이','육개장','치킨','쫄면','닭강정','낙지','잔치국수','비빔냉면','라볶이','순대','김밥','떡국','콩나물해장국',
            '떡','족발','덮밥','돼지불백','만두전골','쌈밥','해물탕','홍합탕','삼겹살','닭꼬치','삼계탕','된장찌개','소고기','갈비찜','비빔밥')
japanese_food=('연어덮밥','우동','샤브샤브','일본식덮밥','소바','일본가정식','초밥','참치회','와규','돈카츠','타코야키','라멘')
chinese_food=('양갈비','짬뽕','짜장면','볶음밥','베이징덕','사천요리','탕수육','훠궈','양꼬치','딤섬','마라탕','깐풍기','꿔바로우')
western_food=('스테이크','샌드위치','피자','리조또','햄버거','파스타','브런치','필라프','오믈렛')
other_country_food=('쌀국수','타코','빠에야','케사디자','브리또')

meat_food=('양꼬치','갈비찜','오리고기','백숙','닭볶음탕','탕수육','꿔바로우','깐풍기','소고기','베이징덕','치킨','뚝배기불고기','돈까스',
        '불고기','돼지불백','곱창','육회','삼계탕','삼겹살','보쌈','훠궈','일본식덮밥','닭꼬치','돼지갈비','족발','닭갈비','와규','양갈비','닭발',
        '돈카츠','돼지목살','닭강정','샤브샤브','스테이크','꼬치구이')
sea_food=('해물탕','해물뚝배기','굴국밥','생선구이','사천요리','어묵','낙지','연어덮밥','초밥','회덮밥','생선조림','장어','매운탕',
        '꼬막정식','회','참치회','조개구이','홍합탕','쭈꾸미','대게','물회','꼬막','게장')
noodle_food=('짬뽕','잔치국수','콩국수','비빔메밀면','칼국수','비빔국수','라면','소바','라볶이','우동','골뱅이소면','짜장면','파스타','쫄면','쌀국수',
            '냉면','비빔냉면','라멘')
rice_food=('꼬막정식','부대찌개','제육덮밥','돈까스','오므라이스','리조또','필라프','쌈밥','된장찌개','김치볶음밥','도시락','회덮밥','황태해장국',
        '카레라이스','뼈해장국','순대국','불고기','뚝배기불고기','굴국밥','비빔밥','순두부찌개','양평해장국','일본식덮밥','초밥','덮밥','콩나물국밥',
        '김치찜','돼지국밥','육개장','콩나물해장국','추어탕','소머리국밥','보리밥','김치찌개','돼지불백','김밥','일본가정식','한정식','볶음밥','연어덮밥',
        '설렁탕','오믈렛','빠에야','쌀밥')
flour_food=('호빵','수제비','만두국','골뱅이소면','라면','비빔국수','떡튀순','길거리음식','떡볶이','잔치국수','라볶이','떡국','떡','우동','타코야키',
        '라멘','짬뽕','짜장면','딤섬','샌드위치','피자','햄버거','파스타','브런치','타코','브리또','케사디자','떡꼬치')
soup_food=('순두부찌개','콩나물해장국','잔치국수','해물탕','만두전골','추어탕','황태해장국','백숙','콩나물국밥','삼계탕','굴국밥','소머리국밥','뼈해장국',
        '양평해장국','우동','칼국수','감자탕','육개장','매운탕','순대국','쌀국수','짬뽕','설렁탕','해물뚝배기','된장찌개','김치찌개','사천요리',
        '홍합탕','부대찌개','라면','떡국','만두국','수제비','라멘','돼지국밥','마라탕')

delivery_food=('치킨','햄버거','족발','보쌈','피자','떡볶이','짜장면','짬뽕','볶음밥','돈까스','닭강정')
cook_food=('카레라이스','만두국','오므라이스','김치찌개','김치볶음밥','라면','불고기','떡국','비빔밥')
class Food(commands.Cog, name='Food'):
    @commands.command(name='뭐먹지')
    async def Roulette_init(self, ctx):
        embed=discord.Embed(title=f"안녕하세요 영양사 Bot입니다 >_<",description=f"아래 선택지중에 원하시는 항목을 말씀해주세요",color=0xf3bb76)
        embed.add_field(name=f"뭐 먹지?", value="배달, 요리, 외식, 안먹을래", inline=True)
        await ctx.send(embed=embed)

        check=1
        while check:
            msg = await ctx.bot.wait_for('message')
            if (ctx.author == msg.author and ctx.channel == msg.channel):
                if (msg.content == '배달'): 
                    await ctx.send("배달음식을 선택하셨습니다")
                    index=random.randint(1,len(delivery_food))
                    
                    embed=discord.Embed(title=f"집에서 편하게 시켜 먹자!",color=0xf3bb76)
                    embed.add_field(name=f"오늘의 음식은??",value=delivery_food[index-1],inline=True)
                    await ctx.send(embed=embed)
                    check=0
                elif (msg.content == '요리'):
                    await ctx.send("요리하기를 선택하셨습니다")
                    index=random.randint(1,len(cook_food))
                    
                    embed=discord.Embed(title=f"간단하게 할 수 있는 음식!",color=0xf3bb76)
                    embed.add_field(name=f"오늘의 음식은??",value=cook_food[index-1],inline=True)
                    await ctx.send(embed=embed)
                    check=0
                elif (msg.content == '외식'):
                    await ctx.send("외식을 선택하셨습니다")
                    country_list=['한식','일식','중식','양식','기타','상관없음']
                    kind_list=['밥','밀가루','면','고기','해산물','국물','상관없음']
                    my_food=set()
                    my_food2=set()
                    while check:
                        embed=discord.Embed(title=f"어떤 음식이 좋으신가요?",color=0xf3bb76)
                        embed.add_field(name=f"원하시는 항목을 말씀해주세요",value=country_list,inline=True)
                        await ctx.send(embed=embed)
                        msg = await ctx.bot.wait_for('message')
                        if (ctx.author == msg.author and ctx.channel == msg.channel):
                            if (msg.content == '한식'):
                                my_food= my_food | set(korean_food)
                                await ctx.send("더 고르시겠어요? (예/아니오)")
                                msg = await ctx.bot.wait_for('message')
                                if (ctx.author == msg.author and ctx.channel == msg.channel and msg.content == '예'):
                                    continue
                                check=0
                            elif (msg.content == '일식'):
                                my_food= my_food | set(japanese_food)
                                await ctx.send("더 고르시겠어요? (예/아니오)")
                                msg = await ctx.bot.wait_for('message')
                                if (ctx.author == msg.author and ctx.channel == msg.channel and msg.content == '예'):
                                    continue
                                check=0
                            elif (msg.content == '중식'):
                                my_food= my_food | set(chinese_food)
                                await ctx.send("더 고르시겠어요? (예/아니오)")
                                msg = await ctx.bot.wait_for('message')
                                if (ctx.author == msg.author and ctx.channel == msg.channel and msg.content == '예'):
                                    continue
                                check=0
                            elif (msg.content == '양식'):
                                my_food= my_food | set(western_food)
                                await ctx.send("더 고르시겠어요? (예/아니오)")
                                msg = await ctx.bot.wait_for('message')
                                if (ctx.author == msg.author and ctx.channel == msg.channel and msg.content == '예'):
                                    continue
                                check=0
                            elif (msg.content == '기타'):
                                my_food= my_food | set(other_country_food)
                                await ctx.send("더 고르시겠어요? (예/아니오)")
                                msg = await ctx.bot.wait_for('message')
                                if (ctx.author == msg.author and ctx.channel == msg.channel and msg.content == '예'):
                                    continue
                                check=0
                            elif (msg.content == '상관없음'):
                                await ctx.send("상관없으시군요?")
                                my_food = set(korean_food) | set(japanese_food) | set(chinese_food) | set(western_food) | set(other_country_food)
                                check=0
                            else:
                                await ctx.send("제대로 골라주세요")

                    await ctx.send("이제 원하시는 종류를 선택해 주세요")
                    check=1
                    while check:
                        embed=discord.Embed(title=f"어떤 음식이 좋으신가요?",color=0xf3bb76)
                        embed.add_field(name=f"원하시는 항목을 말씀해주세요",value=kind_list,inline=True)
                        await ctx.send(embed=embed)
                        msg = await ctx.bot.wait_for('message')
                        if (ctx.author == msg.author and ctx.channel == msg.channel):
                            if (msg.content == '밥'):
                                my_food2=my_food2 | set(rice_food)
                                await ctx.send("더 고르시겠어요? (예/아니오)")
                                msg = await ctx.bot.wait_for('message')
                                if (ctx.author == msg.author and ctx.channel == msg.channel and msg.content == '예'):
                                    continue
                                check=0
                            elif(msg.content == '밀가루'):  #밥','밀가루','면','고기','해산물','국물'
                                my_food2=my_food2 | set(flour_food)
                                await ctx.send("더 고르시겠어요? (예/아니오)")
                                msg = await ctx.bot.wait_for('message')
                                if (ctx.author == msg.author and ctx.channel == msg.channel and msg.content == '예'):
                                    continue
                                check=0
                            elif(msg.content == '면'):
                                my_food2=my_food2 | set(noodle_food)
                                await ctx.send("더 고르시겠어요? (예/아니오)")
                                msg = await ctx.bot.wait_for('message')
                                if (ctx.author == msg.author and ctx.channel == msg.channel and msg.content == '예'):
                                    continue
                                check=0
                            elif(msg.content == '고기'):
                                my_food2=my_food2 | set(meat_food)
                                await ctx.send("더 고르시겠어요? (예/아니오)")
                                msg = await ctx.bot.wait_for('message')
                                if (ctx.author == msg.author and ctx.channel == msg.channel and msg.content == '예'):
                                    continue
                                check=0
                            elif(msg.content == '해산물'):
                                my_food2=my_food2 | set(sea_food)
                                await ctx.send("더 고르시겠어요? (예/아니오)")
                                msg = await ctx.bot.wait_for('message')
                                if (ctx.author == msg.author and ctx.channel == msg.channel and msg.content == '예'):
                                    continue
                                check=0
                            elif(msg.content == '국물'):
                                my_food2=my_food2 | set(soup_food)
                                await ctx.send("더 고르시겠어요? (예/아니오)")
                                msg = await ctx.bot.wait_for('message')
                                if (ctx.author == msg.author and ctx.channel == msg.channel and msg.content == '예'):
                                    continue
                                check=0
                            elif(msg.content == '상관없음'):
                                await ctx.send("상관없으시군요?")
                                my_food2=set(rice_food) | set(flour_food) | set(noodle_food) | set(meat_food) | set(sea_food) | set(soup_food)
                                check=0
                
                    my_food_list=my_food & my_food2
                    my_food_list=list(my_food_list)
                    index=random.randint(1,len(my_food_list))
                    embed=discord.Embed(title=f"외식은 언제나 즐거워~",color=0xf3bb76)
                    embed.add_field(name=f"오늘의 음식은??",value=my_food_list[index-1],inline=True)
                    await ctx.send(embed=embed)

                elif msg.content == '안먹을래':
                    await ctx.send("배고파지시면 언제든지 불러주세요~^^")
                    check=0
                elif check == 2:
                    await ctx.send("항목을 제대로 보고 다시 골라주세요 ㅡㅡ")
                else:
                    await ctx.send("제대로 골라주세요")
                    check = 2
    
    @commands.command(name='한식월드컵')
    async def WolrdCup_init(self, ctx):
        embed=discord.Embed(title=f"안녕하세요 영양사 Bot입니다 >_<",description=f"한식 월드컵 16강입니다.",color=0xf3bb76)
        embed.add_field(name=f"보기가 2가지 나오면 하나를 말씀해주세요",value="시작!", inline=True)
        await ctx.send(embed=embed)

        korean_food_worldCup16=set()
        while len(korean_food_worldCup16) < 16:
            index=random.randint(1,len(korean_food))
            korean_food_worldCup16.add(korean_food[index-1])
        
        korean_food_worldCup16=list(korean_food_worldCup16)
        index=0
        korean_food_worldCup8=set()
        while len(korean_food_worldCup8) < 8:
            embed=discord.Embed(title=f"한식 월드컵 16강",description=f"아래 보기에서 하나를 말씀해주세요",color=0xf3bb76)
            embed.add_field(name=f"₍₍ ◝(・ω・)◟ ⁾⁾",value=korean_food_worldCup16[index]+" / "+korean_food_worldCup16[index+1], inline=True)
            await ctx.send(embed=embed)

            msg = await ctx.bot.wait_for('message')
            if (ctx.author == msg.author and ctx.channel == msg.channel):
                if(msg.content == korean_food_worldCup16[index]):
                    korean_food_worldCup8.add(korean_food_worldCup16[index])
                    index += 2
                elif(msg.content == korean_food_worldCup16[index+1]):
                    korean_food_worldCup8.add(korean_food_worldCup16[index+1])
                    index += 2
                else:
                    await ctx.send("제대로 골라주세요")
                    continue
        await ctx.send("16강 종료!  8강 시작하겠습니다!")
        korean_food_worldCup8=list(korean_food_worldCup8)
        index=0
        korean_food_worldCup4=set()
        while len(korean_food_worldCup4) < 4:
            embed=discord.Embed(title=f"한식 월드컵 8강",description=f"아래 보기에서 하나를 말씀해주세요",color=0xf3bb76)
            embed.add_field(name=f"₍₍ ◝(・ω・)◟ ⁾⁾",value=korean_food_worldCup8[index]+" / "+korean_food_worldCup8[index+1], inline=True)
            await ctx.send(embed=embed)

            msg = await ctx.bot.wait_for('message')
            if (ctx.author == msg.author and ctx.channel == msg.channel):
                if(msg.content == korean_food_worldCup8[index]):
                    korean_food_worldCup4.add(korean_food_worldCup8[index])
                    index += 2
                elif(msg.content == korean_food_worldCup8[index+1]):
                    korean_food_worldCup4.add(korean_food_worldCup8[index+1])
                    index += 2
                else:
                    await ctx.send("제대로 골라주세요")
                    continue
        
        await ctx.send("8강 종료!  4강 시작하겠습니다!")
        korean_food_worldCup4=list(korean_food_worldCup4)
        index=0
        korean_food_worldCup2=set()
        while len(korean_food_worldCup2) < 2:
            embed=discord.Embed(title=f"한식 월드컵 4강",description=f"아래 보기에서 하나를 말씀해주세요",color=0xf3bb76)
            embed.add_field(name=f"₍₍ ◝(・ω・)◟ ⁾⁾",value=korean_food_worldCup4[index]+" / "+korean_food_worldCup4[index+1], inline=True)
            await ctx.send(embed=embed)

            msg = await ctx.bot.wait_for('message')
            if (ctx.author == msg.author and ctx.channel == msg.channel):
                if(msg.content == korean_food_worldCup4[index]):
                    korean_food_worldCup2.add(korean_food_worldCup4[index])
                    index += 2
                elif(msg.content == korean_food_worldCup4[index+1]):
                    korean_food_worldCup2.add(korean_food_worldCup4[index+1])
                    index += 2
                else:
                    await ctx.send("제대로 골라주세요")
                    continue
        
        await ctx.send("4강 종료!  결승 시작하겠습니다!")
        korean_food_worldCup2=list(korean_food_worldCup2)
        index=0
        korean_food_worldCup=set()
        while len(korean_food_worldCup) < 1:
            embed=discord.Embed(title=f"한식 월드컵 결승!",description=f"아래 보기에서 하나를 말씀해주세요",color=0xf3bb76)
            embed.add_field(name=f"₍₍ ◝(・ω・)◟ ⁾⁾",value=korean_food_worldCup2[index]+" / "+korean_food_worldCup2[index+1], inline=True)
            await ctx.send(embed=embed)

            msg = await ctx.bot.wait_for('message')
            if (ctx.author == msg.author and ctx.channel == msg.channel):
                if(msg.content == korean_food_worldCup2[index]):
                    korean_food_worldCup.add(korean_food_worldCup2[index])
                elif(msg.content == korean_food_worldCup2[index+1]):
                    korean_food_worldCup.add(korean_food_worldCup2[index+1])
                else:
                    await ctx.send("제대로 골라주세요")
                    continue
        korean_food_worldCup=list(korean_food_worldCup)
        embed=discord.Embed(title=f"한식 월드컵 우승",description=f"대망의 우승자는 ???",color=0xf3bb76)
        embed.add_field(name=f"°˖✧◝(⁰▿⁰)◜✧˖°",value=korean_food_worldCup[0], inline=True)
        await ctx.send(embed=embed)

    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Food(bot))