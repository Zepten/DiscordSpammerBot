import os
import json
import discord
from discord.ext import commands
from discord.embeds import Embed
from bs4 import BeautifulSoup
import requests
import random

import ipcalc
import hello

# Получение токенов и URL'ов из Heroku
BOT_TOKEN = os.environ.get('BOT_TOKEN')
VK_TOKEN = os.environ.get('VK_TOKEN')
GROUP_ID = os.environ.get('GROUP_ID')
URL34 = os.environ.get('URL34')

# Попытка получения токенов и URL'ов из локального файла (для отладки)
try:
    with open('config.json') as config_file:
        config = json.load(config_file)
        BOT_TOKEN = config['BOT_TOKEN']
        VK_TOKEN = config['VK_TOKEN']
        GROUP_ID = config['GROUP_ID']
        URL34 = config['URL34']
        print("I got all tokens and URL's from config.json!")
except:
    print("I can not find config.json file!")

# Заголовки
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.111 YaBrowser/21.2.1.107 Yowser/2.5 Safari/537.36', 
    'accept': '*/*'
}

# Права для бота
intents = discord.Intents().all()
bot = commands.Bot(command_prefix='-', intents=intents, case_insensitive=True)
bot.remove_command('help')

# Готовность бота к работе
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='-help'))
    print(f'{bot.user.name} is ready!')

# Не найдена команда
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'{ctx.message.author.mention}, я не знаю такой команды. :rolling_eyes: Обратись в `-help`')

# Лог в консоль
@bot.event
async def on_command(ctx):
    print(f'"{ctx.command.name}" was invoked.')

# Очистка сообщений
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=1):
    await ctx.channel.purge(limit=amount+1)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.message.author.mention}, у тебя нет права очищать сообщения :sob:')

# Ping
@bot.command()
async def ping(ctx):
    await ctx.send(f'Мой пинг: {round(bot.latency * 1000)}мс')

# Help
@bot.group(invoke_without_command=True, ignore_extra=False)
async def help(ctx):
    emb = Embed(
        title=':face_with_monocle: Список команд (для любопытных)',
        description='Напиши `-help <имя команды>` для более подробной информации'
    )
    emb.add_field(name='-hi :wave:', value='Поздороваться')
    emb.add_field(name='-anon :detective:', value=f'Анонимизатор')
    emb.add_field(name='-ip :computer:', value='IP-калькулятор')
    emb.add_field(name='-dice :game_die:', value='Бросить кубик')
    emb.add_field(name='-roulette :gun:', value='Русская рулетка')
    emb.add_field(name='-vote :white_check_mark:', value='Голосование')
    emb.add_field(name='-music :musical_note:', value='Музыкальные команды')
    emb.add_field(name='-ord :scroll:', value='Рандомная цитата\nиз ОРД цитатника')
    emb.add_field(name='-stat :bar_chart:', value='Статистика пользователя')
    await ctx.send(embed=emb)

@help.error
async def help_error(ctx, error):
    await ctx.send(f'{ctx.message.author.mention}, не понял, о чем ты. :confused: Напиши `-help`, если сам не понял')

# Поздороваться
@bot.command()
async def hi(ctx):
    author = ctx.message.author
    await ctx.send(f'{random.choice(hello.hello_word)}, {author.mention}')

@help.command()
async def hi(ctx):
    emb = Embed(title='Hi :wave:', 
        description='**Поздороваться**\nПоздороваюсь с тобой на каком-нибудь языке.\nЯ вообще все сделаю по твоему желанию :flushed:')
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
    emb = Embed(title='Anon :detective:', 
        description='**Анонимизатор**\nТы вводишь сообщение, а я делаю так, чтобы никто не узнал о том, что это написал именно ты\n*P.S.: Я ничего не гарантирую :grin:*')
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
    emb = Embed(
        title='IP :computer:',
        description='**IP-калькулятор**\nХз, зачем Паша его сюда вставил, мб больше нечего :cry:',
    )
    emb.add_field(name='Синтаксис', value='`-ip <ip-адрес> <номер маски>`', inline=False)
    emb.add_field(name='Че это такое', value='<ip-адрес> состоит из **4** байт (чисел от 0 до 255), разделенных точкой *(пример: 192.169.0.1)*.\n<номер маски> - это число от 0 до 32.', inline=False)
    emb.add_field(name='Фишки', value='В IP-адрес ты можешь записать меньше 4-х чисел, тогда все остальные я заполню нулями.\nТакже все числа я привожу к диапазону от 0 до 255 *(для IP)* или от 0 до 32 *(для номера маски)*.\nИными словами, ты можешь написать `-ip 999.999.999.999 999`, а я восприму это как `-ip 255.255.255.255 32`.', inline=False)
    await ctx.send(embed=emb)

# Бросить кубики
@bot.command()
async def dice(ctx, n: str = '6'):
    if n == 'game':
        await ctx.send('https://youtu.be/SshZVDtWLdU')
        return
    else:
        try:
            n = int(n)
        except:
            await ctx.send(f'{ctx.message.author.mention}, я не понял, сколько граней у кубика :game_die:')
            return
    
    egg = random.random() <= 0.05
    if n == 6:
        title = 'Детка, я холодный кубик' if egg else 'Бросаю кубик'
    else:
        n = max(2, n)
        title = f'Детка, я холодный кубик с {n} гранями' if egg else f'Бросаю кубик с {n} гранями'
    emb = Embed(
        title = title,
        description = f':game_die: **{random.randint(1, n)}**'
    )
    await ctx.send(embed=emb)
    
@help.command()
async def dice(ctx):
    emb = Embed(
        title='Dice :game_die:',
        description='**Бросить кубик**\nКидаю кубик и говорю, что выпало. Можно настраивать количество граней'
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

# Рандомный пост из ОРД
@bot.command()
async def ord(ctx):
    response = requests.get(
        'https://api.vk.com/method/wall.get',
        params = {
            'owner_id': GROUP_ID, 'count': 1, 'offset': 0,
            'access_token': VK_TOKEN, 'v': '5.130'
        }
    )
    post_count = response.json()['response']['count']
    response = requests.get(
        'https://api.vk.com/method/wall.get',
        params = {
            'owner_id': GROUP_ID, 'count': 1,
            'offset': random.randint(0, post_count - 1),
            'access_token': VK_TOKEN, 'v': '5.130', 'extended': '1'
        }
    )
    content = response.json()['response']['items'][0]['text']
    emb = Embed(
        title = '"' + content + '"',
        description = '© ' + response.json()['response']['groups'][0]['name']
    )
    attachments = response.json()['response']['items'][0]
    try:
        if attachments['attachments'][0]['type'] == 'photo':
            image = attachments['attachments'][0]['photo']['sizes'][-1]['url']
            emb.set_image(url=image)
    except:
        pass
    thumbnail = response.json()['response']['groups'][0]['photo_200']
    emb.set_thumbnail(url=thumbnail)
    emb.color = discord.Color.from_rgb(255, 100, 100)

    await ctx.send(embed=emb)

@ord.error
async def ord_error(ctx, error):
    await ctx.send(':grimacing: Упс... Какая-то ошибка... Не могу показать цитату...')
    
@help.command()
async def ord(ctx):
    emb = Embed(title='Ord :scroll:', 
        description='**Рандомная цитата из ОРД цитатника**\nЯ покажу тебе отборную цитату из самого классного паблика **"ОРД Цитатник"**')
    emb.add_field(name='Синтаксис', value='`-ord`')
    await ctx.send(embed=emb)

# Статистика
@bot.command()
async def stat(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.message.author
    emb = Embed(
        title=f'Статистика пользователя {member.name}', description=member.mention, color=discord.Color.gold()
    )
    emb.set_thumbnail(url=member.avatar_url)
    emb.add_field(name='ID пользователя', value=member.id, inline=True)
    emb.add_field(name='Топ роль', value=member.top_role.mention, inline=True)
    emb.add_field(name='На сервере с', value=member.joined_at.strftime('%d.%m.%Y'), inline=False)
    # emb.add_field(name='Опыт:', value=100, inline=True)
    # emb.add_field(name='Уровень:', value=1, inline=True)
    emb.set_footer(icon_url=ctx.author.avatar_url, text=f'Поинтересовался {ctx.author.name}')
    await ctx.send(embed=emb)

@stat.error
async def time_error(ctx, error):
    await ctx.send(f'{ctx.message.author.mention}, надо упомянуть кого-нибудь, либо написать ник')

@help.command()
async def stat(ctx):
    emb = Embed(
        title='Stat :bar_chart:',
        description=f'**Статистика пользователя**\nПоказываю ID, топ роль и дату подключения на сервер.\nМожно написать чей-нибудь ник, либо упомянуть кого-нибудь (например, меня), либо просто написать `-stat` и получить информацию о себе'
    )
    emb.add_field(name='Синтаксис', value='`-stat <ник, либо упоминание>`\n`-stat`')
    await ctx.send(embed=emb)

def check_is_nsfw(ctx):
    return ctx.message.channel.is_nsfw()

@bot.command(aliases=['r34', 'rule34', 'r'])
@commands.check(check_is_nsfw)
async def rule_34(ctx, *, tags: str = '*'):
    def get_random_posts(url):
        respond_for_img = requests.get(url=url, headers=HEADERS)
        bs = BeautifulSoup(respond_for_img.text, 'html.parser')
        return bs.posts

    def get_any_random_post_url(url):
        resp = requests.get(url=url, headers=HEADERS)
        bs = BeautifulSoup(resp.text, 'html.parser')
        post_id = bs.title.string.split()[-1]
        post_url = URL34+'page=dapi&s=post&q=index&id='+post_id
        return post_url

    if tags == '*':
        post_url = get_any_random_post_url(URL34+'page=post&s=random')
        post = get_random_posts(post_url).post
        image_url = post['file_url'] # Image URL
        post_id = post['id'] # Post ID
    else:
        posts_count = get_random_posts(URL34+'page=dapi&s=post&q=index&limit=1&tags='+tags)['count'] # Posts count
        try:
            post_pid = random.randint(0, int(posts_count) - 1) # Post PID
        except:
            await ctx.send(':sob: Не могу найти такой пост...')
            return
        post = get_random_posts(URL34+'page=dapi&s=post&q=index&limit=1&pid='+str(post_pid)+'&tags='+tags).post # Post object
        image_url = post['file_url'] # Image URL
        post_id = post['id'] # Post ID

    print(f'Sending post ID{post_id}')
    emb = Embed()
    if tags != '*':
        emb.title='Rule34: '+tags
        emb.description = f'Количество постов с этим тэгом: **{posts_count}**\n'
    else:
        emb.title='Rule34: случайный пост'
    emb.set_author(name=f'ID: {post_id}', url=f'{URL34}page=post&s=view&id={post_id}')
    emb.set_image(url=image_url)
    emb.set_footer(text='Тэги: '+post['tags'])

    await ctx.message.delete()
    await ctx.send(embed=emb)

@rule_34.error
async def rule_34(ctx, error):
    if not check_is_nsfw(ctx):
        await ctx.send(':flushed: Нельзя отправлять такое не в NSFW канал...')

# Запуск бота
bot.run(BOT_TOKEN)