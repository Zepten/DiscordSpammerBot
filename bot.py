import config
import ipcalc
import hello

import discord
from discord.ext import commands
import requests
import random

# Права для бота
intents = discord.Intents().all()
bot = commands.Bot(command_prefix='-', intents=intents, case_insensitive=True)
bot.remove_command('help')

# Готовность бота к работе
@bot.event
async def on_ready():
    print(f'{bot.user.name} is ready!')

# Не найдена команда
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'{ctx.message.author.mention}, не понял, о чем ты. :confused: Напиши `-help`, если сам не понял')

# Help
@bot.group(invoke_without_command=True)
async def help(ctx):
    emb = discord.Embed(
        title=':face_with_monocle: Список команд (для любопытных)',
        description='Напиши `-help <имя команды>` для более подробной информации'
    )
    emb.add_field(name='hi :wave:', value='Поздороваться')
    emb.add_field(name='anon :detective:', value=f'Сказать что-то\nот моего имени')
    emb.add_field(name='ip :computer:', value='IP-калькулятор')
    emb.add_field(name='dice :game_die:', value='Бросить кубики')
    emb.add_field(name='roulette :gun:', value='Русская рулетка')
    emb.add_field(name='vote :white_check_mark:', value='Голосование')
    emb.add_field(name='music :musical_note:', value='Музыкальные команды')
    emb.add_field(name='ord :scroll:', value='Рандомная цитата\nиз ОРД цитатника')
    emb.add_field(name='time :alarm_clock:', value='Время на сервере')
    await ctx.send(embed=emb)

# Поздороваться
@bot.command()
async def hi(ctx):
    author = ctx.message.author
    await ctx.send(f'{random.choice(hello.hello_word)}, {author.mention}')

@help.command()
async def hi(ctx):
    emb = discord.Embed(title='Hi :wave:', 
        description='Поздороваюсь с тобой по твоему желанию.\nЯ вообще все сделаю по твоему желанию :flushed:')
    emb.add_field(name='Синтаксис', value='`-hi`')
    await ctx.send(embed=emb)

# Сказать от имени бота
@bot.command()
async def anon(ctx, *, arg):
    await ctx.message.delete()
    await ctx.send('**Кто-то сказал:** '+arg)

@anon.error
async def anon_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f':clap: Поздравляю, {ctx.message.author.mention} ты спалился. *Надо сообщение написать, а не просто `-anon`*')

@help.command()
async def anon(ctx):
    emb = discord.Embed(title='Anon :detective:', 
        description='Ты вводишь сообщение, а я делаю так, чтобы никто не узнал о том, что это написал именно ты\n*P.S.: Я ничего не гарантирую :grin:*')
    emb.add_field(name='Синтаксис', value='`-anon <сообщение>`')
    await ctx.send(embed=emb)

# IP-калькулятор
@bot.command(ignore_extra=False)
async def ip(ctx, ip: str, bitmask: int):
    # Парсинг IP
    try:
        ip = list(map(int, ip.split('.')))
    except:
        await ctx.send(f'{ctx.message.author.mention}, че за бред? :face_with_raised_eyebrow: У тебя в IP-адресе какая-то неразбериха')
        return
    if len(ip) > 4:
        await ctx.send(f'{ctx.message.author.mention}, IP-адрес состоит из **4** байт, а у тебя написано явно побольше')
        return
    while len(ip) < 4:
        ip.append(0)
    
    # Клэмпинг IP
    ip = [max(0, min(i, 255)) for i in ip]

    # Клэмпинг номера маски
    bitmask = max(0, min(bitmask, 32))

    text = f'{ctx.message.author.mention}, готово :thumbsup:\n'
    text += ipcalc.calculate(ip, bitmask)

    await ctx.send(text)

@ip.error
async def ip_error(ctx, error):
    if isinstance(error, commands.TooManyArguments):
        await ctx.send(f'{ctx.message.author.mention}, :face_with_raised_eyebrow: Че-то многовато всего... Обратись-ка в `-help ip`')
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.message.author.mention}, чего-то не хватает. :face_with_raised_eyebrow: Обратись-ка в `-help ip`')
        return
    if isinstance(error, commands.BadArgument):
        await ctx.send(f'{ctx.message.author.mention}, номер маски - это число, но видимо ты другого мнения')
        return

@help.command()
async def ip(ctx):
    emb = discord.Embed(
        title='IP :computer:',
        description='IP-калькулятор. Хз, зачем Паша его сюда вставил, мб больше нечего :cry:',
    )
    emb.add_field(name='Синтаксис', value='`-ip <ip-адрес> <номер маски>`', inline=False)
    emb.add_field(name='Че это такое', value='<ip-адрес> состоит из **4** байт (чисел от 0 до 255), разделенных точкой *(пример: 192.169.0.1)*.\n<номер маски> - это число от 0 до 32.', inline=False)
    emb.add_field(name='Фишки', value='В IP-адрес ты можешь записать меньше 4-х чисел, тогда все остальные я заполню нулями.\nТакже все числа я привожу к диапазону от 0 до 255 *(для IP)* или от 0 до 32 *(для номера маски)*.\nИными словами, ты можешь написать `-ip 999.999.999.999 999`, а я восприму это как `-ip 255.255.255.255 32`.', inline=False)
    await ctx.send(embed=emb)

# Бросить кубики
@bot.command()
async def dice(ctx, n: int = 6):
    egg = random.random() <= 0.05
    if n == 6:
        title = 'Детка, я холодный кубик' if egg else 'Бросаю кубик'
    else:
        n = max(2, n)
        title = f'Детка, я холодный кубик с {n} гранями' if egg else f'Бросаю кубик с {n} гранями'
    emb = discord.Embed(
        title = title,
        description = f':game_die: **{random.randint(1, n)}**'
    )
    await ctx.send(embed=emb)
    
@dice.error
async def dice_error(ctx, error):
    await ctx.send(f'{ctx.message.author.mention}, я не понял, сколько граней у кубика :game_die:')
    
@help.command()
async def dice(ctx):
    emb = discord.Embed(
        title='Dice :game_die:',
        description='Кидаю кубик и говорю, что выпало. Можно настраивать количество граней'
    )
    emb.add_field(name='Синтаксис', value='`-dice`\n`-dice <количество граней>`')
    await ctx.send(embed=emb)

# Русская рулетка
@bot.command()
async def roulette(ctx):
    await ctx.send('Команда `-roulette` в разработке :tools:')

@roulette.error
async def roulette_error(ctx, error):
    return
    
@help.command()
async def roulette(ctx):
    await ctx.send('Команда `-help roulette` в разработке :tools:')

# Голосование
@bot.command()
async def vote(ctx):
    await ctx.send('Команда `-vote` в разработке :tools:')

@vote.error
async def vote_error(ctx, error):
    return
    
@help.command()
async def vote(ctx):
    await ctx.send('Команда `-help vote` в разработке :tools:')

# Музыкальные команды
@bot.command()
async def music(ctx):
    await ctx.send('Команда `-music` в разработке :tools:')

@music.error
async def music_error(ctx, error):
    return
    
@help.command()
async def music(ctx):
    await ctx.send('Команда `-help music` в разработке :tools:')

# Рандомная цитата из ОРД цитатника
@bot.command()
async def ord(ctx):
    url = requests.get(
        'https://api.vk.com/method/wall.get',
        params = {
            'owner_id': config.GROUP_ID, 'count': 1, 'offset': 0,
            'access_token': config.VK_TOKEN, 'v': '5.130'
        }
    )
    post_count = url.json()['response']['count']
    url = requests.get(
        'https://api.vk.com/method/wall.get',
        params = {
            'owner_id': config.GROUP_ID, 'count': 1,
            'offset': random.randint(0, post_count - 1),
            'access_token': config.VK_TOKEN, 'v': '5.130'
        }
    )
    content = url.json()['response']['items'][0]['text']
    emb = discord.Embed(
        title = '"' + content + '"',
        description = '© ОРД Цитатник'
    )
    emb.set_thumbnail(url='https://d.radikal.ru/d33/2103/21/2c590a3e5b91.jpg')
    emb.color = discord.Color.from_rgb(255, 100, 100)
    await ctx.send(embed=emb)

@ord.error
async def ord_error(ctx, error):
    await ctx.send(':grimacing: Упс... Какая-то ошибка... Не могу показать цитату...')
    
@help.command()
async def ord(ctx):
    emb = discord.Embed(title='Ord :scroll:', 
        description='Я покажу тебе отборную цитату из самого классного паблика **"ОРД Цитатник"**')
    emb.add_field(name='Синтаксис', value='`-ord`')
    await ctx.send(embed=emb)

# Время на сервере
@bot.command()
async def time(ctx):
    await ctx.send('Команда `-time` в разработке :tools:')

@time.error
async def time_error(ctx, error):
    return
    
@help.command()
async def time(ctx):
    await ctx.send('Команда `-time ord` в разработке :tools:')

# Лог в консоль
@bot.event
async def on_command(ctx):
    print(f'"{ctx.command.name}" was invoked.')

# Запуск бота
bot.run(config.BOT_TOKEN)