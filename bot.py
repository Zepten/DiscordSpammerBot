from discord.flags import Intents
import config
import ipcalc
import hello

import typing
from discord import message
import discord
from discord.ext import commands
from discord import Embed
from discord.ext.commands import Bot
from asyncio import sleep
import random

# Права для бота
intents = discord.Intents().all()
bot = commands.Bot(command_prefix=config.PREFIX, intents=intents)
bot.remove_command('help')

# Готовность бота к работе
@bot.event
async def on_ready():
    print(f'{bot.user.name} is ready!')

# Help
@bot.group(invoke_without_command=True)
async def help(ctx):
    emb = discord.Embed(title=':face_with_monocle: Для любопытных',
        description='Напиши `-help <имя команды>` для более подробной информации')
    emb.add_field(name='hi :wave:', value='Поздороваться')
    emb.add_field(name='anon :detective:', value='Сказать что-то от моего имени')
    emb.add_field(name='ip :computer:', value='IP-калькулятор')
    await ctx.send(embed=emb)

# Поздороваться
@bot.command()
async def hi(ctx):
    author = ctx.message.author
    await ctx.send(f'{random.choice(hello.hello_word)}, {author.mention}')

@help.command()
async def hi(ctx):
    emb = discord.Embed(title='Hi :wave:', 
        description='Поздороваюсь с тобой на всех языках мира по твоему желанию.\nЯ вообще все сделаю по твоему желанию :flushed:')
    emb.add_field(name='Синтаксис', value='-hi')
    await ctx.send(embed=emb)

# Сказать от имени бота
@bot.command()
async def anon(ctx, *, arg):
    await ctx.message.delete()
    await ctx.send(arg)

@help.command()
async def anon(ctx):
    emb = discord.Embed(title='Anon :detective:', 
        description='Ты вводишь сообщение, а я делаю так, чтобы никто не узнал о том, что это написал именно ты\n*P.S.: Я ничего не гарантирую :grin:*')
    emb.add_field(name='Синтаксис', value='-anon <сообщение>')
    await ctx.send(embed=emb)

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

@help.command()
async def ip(ctx):
    emb = discord.Embed(title='IP :computer:', 
        description='Хз, зачем Паша его сюда вставил, мб больше нечего :cry:')
    emb.add_field(name='Синтаксис', value='-ip <ip-адрес> <номер маски>')
    await ctx.send(embed=emb)

# Запуск бота
bot.run(config.TOKEN)