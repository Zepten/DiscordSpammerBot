import config
import ipcalc

import typing
from discord import message
import discord
from discord.ext import commands
from discord import Embed
from discord.ext.commands import Bot
from asyncio import sleep
import random

# Права для бота
intents = discord.Intents(config.INTENTS)
bot = commands.Bot(command_prefix = config.PREFIX, intents=intents)

# Help
@bot.command()
async def help(ctx):
    text =  '**Вот что я умею:**\n'
    text += ':wave: `-hi` - Поздороваться\n'
    text += ':detective: `-anon` - Сказать что-то от моего имени *(твое сообщение удалится)*\n'
    text += ':computer: `-ip` - IP-калькулятор (хз, зачем Паша его сюда вставил, мб больше нечего xd)\n'
    text += ':yum: `-fanfic` - Рассказать мой знаменитый фанфик :heart: :blue_heart:'
    await ctx.send(text)

# Поздороваться
@bot.command()
async def hi(ctx):
    author = ctx.message.author
    hello_word = [
        'Привет', 'Здорова', 'Здравствуй',
        'Моё почтение', 'Hello', 'Приветствую'
    ]
    await ctx.send(f'{random.choice(hello_word)}, {author.mention}')

# Сказать от имени бота
@bot.command()
async def say(ctx, *, arg):
    await ctx.message.delete()
    await ctx.send(arg)

# IP-калькулятор
@bot.command()
async def ip(ctx, *arg):
    if len(arg) == 2:
        await ctx.send(ipcalc.calculate(arg[0], arg[1]))
    elif len(arg) == 1:
        await ctx.send('Допиши `<номер маски>`, а то я хз, что с этим делать)')
    elif len(arg) == 0:
        await ctx.send('Гайд как ввести команду **ip**: ```-ip <ip-адрес> <номер маски>```')
    elif len(arg) > 2:
        await ctx.send('В глаза долбишься? Надо только 2 аргумента.')

# Запуск бота
bot.run(config.TOKEN)