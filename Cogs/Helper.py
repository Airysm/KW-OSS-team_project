# -*- coding: utf-8 -*-
# helper.py

import discord
from discord.ext import commands


class Helper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='명령어', help='도움말', usage='!!help')
    async def help_command(self, ctx, func=None):
        cogList = ['R6Stat', 'LoLStat', 'PUBGStat', 'Steam', 'Team', 'MiniRPG', 'Drive']
        if func is None:
            embed = discord.Embed(title='Help', description='(╯°□°）╯︵ ┻━┻')
            for x in cogList:
                cogData = self.bot.get_cog(x)
                commandList = cogData.get_commands()
                embed.add_field(name=x, value='\n'.join([command.name for command in commandList]), inline=True)
            await ctx.send(embed=embed)
        else:
            isCommandNone = True
            for _title, cog in self.bot.cogs.items():
                if not isCommandNone:
                    break
                else:
                    for title in cog.get_commands():
                        if title.name == func:
                            cmd = self.bot.get_commands(title.name)
                            embed = discord.Embed(title=f'명령어 : {cmd}', description=cmd.help)
                            embed.add_field(name='사용법', value=cmd.usage)
                            await ctx.send(embed=embed)
                            isCommandNone=False
                            break
            if isCommandNone:
                if func in cogList:
                    cogData = self.bot.get_cog(func)
                    commandList = cogData.get_commands()
                    embed = discord.Embed(title=f'{cogData.qualified_name}', description=cogData.description)
                    embed.add_field(name='명령어들', value='\n'.join([command.name for command in commandList]))
                    await ctx.send(embed=embed)
            else:
                await ctx.send('그런 이름의 명령어나 카테고리는 없습니다.')
        


def setup(bot):
    bot.add_cog(Helper(bot))
