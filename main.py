import asyncio
from asyncio.tasks import current_task
import discord
import os
from os import system

from discord import FFmpegPCMAudio
from discord import channel
from discord import client
from discord import colour
from discord import embeds
from discord.embeds import Embed
from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument
from cfg import config

import datetime

import requests
import random

import sqlite3
conn = sqlite3.connect("Discord.db")
cursor = conn.cursor()

import json

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = config.settings['prefix'], intents = intents, case_insentitive = True)

@bot.event
async def on_ready():
    print("bot has been runned")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="print > before using commands"))
    for guild in bot.guilds:
        if guild.id == config.your_guild_id:
            for member in guild.members:
                cursor.execute(f"SELECT id FROM users where id = {member.id};")
                if cursor.fetchone() == None:
                    cursor.execute(f'INSERT INTO users VALUES ({member.id}, "{member.name}", "<@{member.id}>", 0, "S", "[]", 1, 0, 0);')
                    conn.commit()
                else:
                    pass
                cursor.execute(f"select id from work where id = {member.id};")
                if cursor.fetchone() == None:
                    cursor.execute(f'insert into work values ({member.id}, {config.year}, {config.month}, {config.day}, {config.hour}, {config.minute}, {config.second})')
                    conn.commit()
                else:
                    pass
                cursor.execute(f"select id from hour where id = {member.id};")
                if cursor.fetchone() == None:
                    cursor.execute(f'insert into hour values ({member.id}, {config.year}, {config.month}, {config.day}, {config.hour}, {config.minute}, {config.second})')
                    conn.commit()
                else:
                    pass
                cursor.execute(f"select id from rob where id = {member.id};")
                if cursor.fetchone() == None:
                    cursor.execute(f'insert into rob values ({member.id}, {config.year}, {config.month}, {config.day}, {config.hour}, {config.minute}, {config.second})')
                    conn.commit()
                else:
                    pass
        print("Joined {}".format(guild.name))

@bot.event
async def on_guild_join(guild):
    print(guild.name)

@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel.id == config.id_of_private_channel_create:
        for guild in bot.guilds:
            maincategory = discord.utils.get(guild.categories, id = config.private_channels_category)
            channel2 = await guild.create_voice_channel(name=member.display_name, category = maincategory)
            await channel2.set_permissions(member, connect = True, mute_members = True, manage_channels = True)
            await member.move_to(channel2)
            def check(x, y, z):
                return len(channel2.members) == 0
            await bot.wait_for('voice_state_update', check=check)
            await channel2.delete()

#member join/remove chapter
@bot.event
async def on_member_join(member):
    for guild in bot.guilds:
        if guild.id == config.your_guild_id:
            channel = bot.get_channel(config.settings['channel_welcome_id'])
            role = discord.utils.get(member.guild.roles, id = config.ranked_roles[5])
            await member.add_roles(role)
            text = 'приветствуем {} в наших рядах!'.format(member.mention)
            await channel.send(embed = discord.Embed( color = discord.Color.dark_blue(), title = '+1 на сервере! :partying_face:', description = text))
            cursor.execute(f"SELECT id FROM users where id = {member.id};")
            if cursor.fetchone() == None:
                cursor.execute(f'INSERT INTO users VALUES ({member.id}, "{member.name}", "<@{member.id}>", 0, "S", "[]", 1, 0, 0);')
                conn.commit()
            else:
                pass
            cursor.execute(f"select id from work where id = {member.id};")
            if cursor.fetchone() == None:
                cursor.execute(f'insert into work values ({member.id}, {config.year}, {config.month}, {config.day}, {config.hour}, {config.minute}, {config.second})')
                conn.commit()
            else:
                pass
            cursor.execute(f"select id from hour where id = {member.id};")
            if cursor.fetchone() == None:
                cursor.execute(f'insert into hour values ({member.id}, {config.year}, {config.month}, {config.day}, {config.hour}, {config.minute}, {config.second})')
                conn.commit()
            else:
                pass
            cursor.execute(f"select id from rob where id = {member.id};")
            if cursor.fetchone() == None:
                cursor.execute(f'insert into rob values ({member.id}, {config.year}, {config.month}, {config.day}, {config.hour}, {config.minute}, {config.second})')
                conn.commit()
            else:
                pass

@bot.event
async def on_member_remove(member):
    if member.guild.id == config.your_guild_id:
        channel = bot.get_channel(config.settings['channel_welcome_id'])
        cursor.execute(f'delete from users where id = {member.id}')
        conn.commit()
        await channel.send(embed = discord.Embed(color = discord.Color.dark_red(), title = '-1 на сервере :(', description = f'прощай, {member.mention}'))

#gif & hello chapter
@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.mention}!')

@bot.command(help = "обнимает указанного пользователя")
async def hug(ctx, member: discord.Member):
    response = requests.get('https://some-random-api.ml/animu/hug')
    json_data = json.loads(response.text)
    text = '{} обнимает'.format(ctx.author.mention)
    text += ' {}!'.format(member.mention)
    embed = discord.Embed(color = 0xa2b6a2, description = text)
    embed.set_image(url = json_data['link'])
    await ctx.send(embed = embed)

@bot.command(help = "гладит указанного пользователя")
async def pat(ctx, member: discord.Member):
    response = requests.get('https://some-random-api.ml/animu/pat')
    json_data = json.loads(response.text)
    text = '{} гладит'.format(ctx.author.mention)
    text += ' {}!'.format(member.mention)
    embed = discord.Embed(color = 0xa2b6a2, description = text)
    embed.set_image(url = json_data['link'])
    await ctx.send(embed = embed)

@bot.command(help = "целует указанного пользователя")
async def kiss(ctx, member: discord.Member):
    action = 'anime kiss'
    randomint = random.randint(0, 50)
    response = requests.get('https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s' % (action, config.settings['tenor_api_key'], 50))
    json_data = json.loads(response.content)
    text = '{} целует'.format(ctx.author.mention)
    text += ' {}!'.format(member.mention)
    embed = discord.Embed(color = 0xa2b6a2, description = text)
    embed.set_image(url = json_data['results'][randomint]['media'][0]['gif']['url'])
    await ctx.send(embed = embed)

@bot.command(help = "бьет указанного пользователя")
async def punch(ctx, member: discord.Member):
    action = 'anime punch'
    randomint = random.randint(0, 50)
    response = requests.get('https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s' % (action, config.settings['tenor_api_key'], 50))
    json_data = json.loads(response.content)
    text = '{} бьет'.format(ctx.author.mention)
    text += ' {}!'.format(member.mention)
    embed = discord.Embed(color = 0xa2b6a2, description = text)
    embed.set_image(url = json_data['results'][randomint]['media'][0]['gif']['url'])
    await ctx.send(embed = embed)

@bot.command(help = "кидает гифку по указанной теме")
async def gif(ctx, *, theme):
    action = theme
    response = requests.get('https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s' % (action, config.settings['tenor_api_key'], 50))
    json_data = json.loads(response.content)
    
    randomint = random.randint(0, min(20, len(json_data['results'])))
    text = 'рандомная гифка по теме {}'.format(theme)
    embed = discord.Embed(color = 0xa2b6a2, description = text)
    embed.set_image(url = json_data['results'][randomint]['media'][0]['gif']['url'])
    await ctx.send(embed = embed)

@bot.command(help = "кидает гифку с котиком")
async def kotik(ctx):
    action = 'kitty'
    randomint = random.randint(0, 50)
    response = requests.get('https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s' % (action, config.settings['tenor_api_key'], 50))
    json_data = json.loads(response.content)
    embed = discord.Embed(colour = discord.Color.dark_purple(), title = 'внимание, котик')
    embed.set_image(url = json_data['results'][randomint]['media'][0]['gif']['url'])
    await ctx.send(embed = embed)

#configuration chapter: ban, mute, clear, kick, unmute - all need "administrator" status
@bot.command(pass_context = True, help = "очищает указанное количество сообщений")
@commands.has_permissions(administrator = True)
async def clearmsg(ctx, amount: int):
    await ctx.channel.purge(limit = amount)
    embed = discord.Embed(color = 0x0c0c0c, description = f':white_check_mark: Удалено {amount} сообщений, {ctx.author.mention}')
    await ctx.send(embed = embed)
@clearmsg.error
async def clearmsg_error(ctx, error):
    if isinstance(error, commands,MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, количество сообщений укажи')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention}, ты не модер')

@bot.command(pass_context = True, help = "кикает указанного пользователя")
@commands.has_permissions(administrator = True)
async def kick(ctx, member: discord.Member, *, reason = None):
    embed = discord.Embed(title = 'кикнули, представляешь?', colour = discord.Color.dark_gold())
    await ctx.channel.purge(limit = 1)

    await member.kick(reason = reason)

    embed.set_author(name = member.name, icon_url = member.avatar_url)
    embed.add_field(name = "кикнули :(", value = 'до скорой встречи, {}'.format(member.mention))
    embed.set_footer(text = 'был кикнут администратором {}'.format(ctx.author.name), icon_url = ctx.author.avatar_url)

    await ctx.send(embed = embed)
@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, укажи участника')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention}, ты не модер')

@bot.command(pass_context = True, help = "банит указанного пользователя")
@commands.has_permissions(administrator = True)
async def ban(ctx, member: discord.Member, *, reason = None):
    embed = discord.Embed(title = 'забанили, представляешь?', colour = discord.Color.red())
    await ctx.channel.purge(limit = 1)

    await member.ban(reason = reason)

    embed.set_author(name = member.name, icon_url = member.avatar_url)
    embed.add_field(name = 'забанили :(', value = 'прощай, {}'.format(member.mention))
    embed.set_footer(text = 'был забанен администратором {}'.format(ctx.author.name), icon_url = ctx.author.avatar_url)

    await ctx.send(embed = embed)
@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, укажи участника')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention}, ты не модер')

@bot.command(pass_context = True, help = "выдает мут указанному пользователю")
@commands.has_permissions(administrator = True)
async def mute(ctx, member: discord.Member):
    embed = discord.Embed(title = 'ты теперь в муте, клоун', colour = discord.Color.red())
    await ctx.channel.purge(limit = 1)
    if ctx.guild.id == config.your_guild_id:
        mute_role = discord.utils.get(ctx.message.guild.roles, id = config.id_role_muted)

    await member.add_roles(mute_role)

    embed.set_author(name = member.name, icon_url = member.avatar_url)
    embed.add_field(name = 'вас никто не слышит', value = 'еще услышимся, {}'.format(member.mention))
    embed.set_footer(text = 'был замучен администратором {}'.format(ctx.author.name), icon_url = ctx.author.avatar_url)

    await ctx.send(embed = embed)
@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, укажи участника')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention}, ты не модер')

@bot.command(pass_context = True, help = "снимает мут с указанного пользователя")
@commands.has_permissions(administrator = True)
async def unmute(ctx, member: discord.Member):
    embed = discord.Embed(title = 'ура, размутили', colour = discord.Color.blue())
    await ctx.channel.purge(limit = 1)
    if ctx.guild.id == config.your_guild_id:
        mute_role = discord.utils.get(ctx.message.guild.roles, id = config.id_role_muted)
    await member.remove_roles(mute_role)

    embed.set_author(name = member.name, icon_url = member.avatar_url)
    embed.add_field(name = 'поздравляем!!!', value = 'теперь вы не немой, {}'.format(member.mention))
    embed.set_footer(text = 'был размучен администратором {}'.format(ctx.author.name), icon_url = ctx.author.avatar_url)

    await ctx.send(embed = embed)
@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, укажи участника')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention}, ты не модер')

@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    if payload.message_id != config.role_message_id:
        return

    for gld in bot.guilds:
        if gld.id == config.your_guild_id:
            guild = bot.get_guild(gld.id)
    if guild is None:
        return

    try:
        role_id = config.emoji_to_role[payload.emoji]
    except KeyError:
        print(payload.emoji)
        return

    role = guild.get_role(role_id)
    if role is None:
        return

    try:
        await payload.member.add_roles(role)
    except discord.HTTPException:
        pass
@bot.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    if payload.message_id != config.role_message_id:
        return
    for gld in bot.guilds:
        if gld.id == config.your_guild_id:
            guild = bot.get_guild(gld.id)
    if guild is None:
        return

    try:
        role_id = config.emoji_to_role[payload.emoji]
    except KeyError:
        return

    role = guild.get_role(role_id)
    if role is None:
        return
    member = guild.get_member(payload.user_id)
    if member is None:
        return

    try:
        await member.remove_roles(role)
    except discord.HTTPException:
        pass

@bot.event
async def on_message(message):
    if message.author.id == 842163794683887636:
        return
    for guild in bot.guilds:
        if guild.id == config.your_guild_id:
            role_0 = guild.get_role(config.ranked_roles[0]) # 40
            role_1 = guild.get_role(config.ranked_roles[1]) # 30
            role_2 = guild.get_role(config.ranked_roles[2]) #20
            role_3 = guild.get_role(config.ranked_roles[3]) #10
            role_4 = guild.get_role(config.ranked_roles[4]) #5
            role_5 = guild.get_role(config.ranked_roles[5])
            if len(message.content) > 6:
                for row in cursor.execute(f"SELECT xp, lvl FROM users where id={message.author.id};"):
                    expi = row[0] + random.randint(10, 40)
                    cursor.execute(f'UPDATE users SET xp={expi} where id={message.author.id};')
                    conn.commit()
                    i = 1
                    while (((i ** 2) * 100) < (row[0])):
                        i += 1
                    lv = i                    
                    if row[1] < lv:
                        await message.channel.send(f'левел ап, {message.author.mention}!')
                        cursor.execute(f'UPDATE users SET lvl={lv} where id={message.author.id};')
                        conn.commit()
                    if lv >= 40:
                        await message.author.add_roles(role_0)
                        await message.author.remove_roles(role_1)
                        await message.author.remove_roles(role_2)
                        await message.author.remove_roles(role_3)
                        await message.author.remove_roles(role_4)
                        await message.author.remove_roles(role_5)
                    elif lv >= 30:
                        await message.author.add_roles(role_1)
                        await message.author.remove_roles(role_2)
                        await message.author.remove_roles(role_3)
                        await message.author.remove_roles(role_4)
                        await message.author.remove_roles(role_5)
                    elif lv >= 20:
                        await message.author.add_roles(role_2)
                        await message.author.remove_roles(role_3)
                        await message.author.remove_roles(role_4)
                        await message.author.remove_roles(role_5)
                    elif lv >= 10:
                        await message.author.add_roles(role_3)
                        await message.author.remove_roles(role_4)
                        await message.author.remove_roles(role_5)
                    elif lv >= 5:
                        await message.author.add_roles(role_4)
                        await message.author.remove_roles(role_5)
                    else:
                        pass
            await bot.process_commands(message)

@bot.command(help = "меняет количество денег на передаваемое значение")
@commands.has_permissions(administrator = True)
async def set_money(ctx, member: discord.Member, money):
    intmoney = int(money)
    for guild in bot.guilds:
        if guild.id == config.your_guild_id:
            cursor.execute(f'update users set money = {intmoney} where id = {member.id};')
            conn.commit()
            print(guild.id)
            embed = discord.Embed(colour = discord.Color.green(), description = f":white_check_mark: количество денег пользователя {member.mention} установлено на значение {intmoney}")
            await ctx.send(embed = embed)
@set_money.error
async def set_money_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, укажи участника и/или количество денег')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention}, ты не модер')

@bot.command(help = "добавляет указанное количество денег пользователю")
@commands.has_permissions(administrator = True)
async def add_money(ctx, member: discord.Member, money: int):
    for guild in bot.guilds:
        if guild.id == config.your_guild_id:
            for row in cursor.execute(f"select money from users where id = {member.id};"):
                balance = row[0]
            cursor.execute(f'update users set money = {balance + money} where id = {member.id};')
            conn.commit()
            await ctx.send(embed = discord.Embed(colour = discord.Color.green(), description = f":white_check_mark: добавлено {money} :moneybag: пользователю {member.mention}"))
@add_money.error
async def add_money_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, укажи участника и/или количество денег')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention}, ты не модер')

xcounter = 0
def issue(meaning: int, value: str):
    global xcounter
    if value == "odd":
        xcounter = 2
        return (meaning % 2 == 1)
    elif value == "even":
        xcounter = 2
        return (meaning % 2 == 0)
    elif value == "red":
        xcounter = 2
        return (meaning in config.red)
    elif value == "green":
        xcounter = 37
        return (meaning in config.green)
    elif value == "black":
        xcounter = 2
        return (meaning in config.black)
    else:
        xcounter = 37
        return (meaning == int(value))

@bot.command(help = 'игра "рулетка": >roulette [сумма ставки] [исходы: odd|even (чет / нечет), red|black|green, число от 0 до 36')
async def roulette(ctx, count, *, value):
    balance = int(count)
    for guild in bot.guilds:
        if guild.id == config.your_guild_id:
            number = random.randint(0, 36)
            for row in cursor.execute(f"select money from users where id = {ctx.author.id};"):
                if row[0] < balance:
                    embed = discord.Embed(colour = discord.Color.red(), title = "ошибка", description = f"{ctx.author.mention}, у вас недостаточно средств на вашем счете")
                    await ctx.send(embed = embed)
                    return
                cursor.execute(f'update users set money = {row[0] - balance} where id = {ctx.author.id};')
                conn.commit()
            for row in cursor.execute(f"select money from users where id = {ctx.author.id};"):
                if issue(number, value):
                    cursor.execute(f'update users set money = {row[0] + balance * xcounter} where id = {ctx.author.id};')
                    conn.commit()
                    embed = discord.Embed(colour = discord.Color.green(), title = "поздравляем!", description = f"{ctx.author.mention}, вы выиграли {balance * xcounter} :moneybag:")
                    await ctx.send(embed = embed)
                else:
                    embed = discord.Embed(colour = discord.Color.green(), title = "в следующий раз повезет!", description = f"{ctx.author.mention}, вы проиграли {balance} :moneybag:")
                    await ctx.send(embed = embed)
@roulette.error
async def roulette_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, укажи количество денег или исход')

@bot.command(help = "позволяет купить опыт в отношении 1 к 1")
async def buy_xp(ctx, xp):
    exp = int(xp)
    for guild in bot.guilds:
        if guild.id == config.your_guild_id:
            role_0 = guild.get_role(config.ranked_roles[0]) # 40
            role_1 = guild.get_role(config.ranked_roles[1]) # 30
            role_2 = guild.get_role(config.ranked_roles[2]) #20
            role_3 = guild.get_role(config.ranked_roles[3]) #10
            role_4 = guild.get_role(config.ranked_roles[4]) #5
            role_5 = guild.get_role(config.ranked_roles[5])
            for row in cursor.execute(f"select xp, money, lvl from users where id = {ctx.author.id};"):
                if row[1] < exp:
                    embed = discord.Embed(colour = discord.Color.red(), title = "ошибка", description = "недостаточно средств на вашем счете")
                    await ctx.send(embed = embed)
                    return
                else:
                    i = 1
                    while (((i ** 2) * 100) < (exp + row[0])):
                        i += 1
                        print(i)
                    lv = i
                    new_xp = row[0] + exp
                    new_money = row[1] - exp
                    cursor.execute(f'update users set xp = {new_xp}, money = {new_money} where id = {ctx.author.id};')
                    conn.commit()
                    if row[1] < lv:
                        await ctx.channel.send(f'левел ап, {ctx.author.mention}!')
                        cursor.execute(f'UPDATE users SET lvl={lv} where id={ctx.author.id};')
                        conn.commit()
                    if lv >= 40:
                        await ctx.author.add_roles(role_0)
                        await ctx.author.remove_roles(role_1)
                        await ctx.author.remove_roles(role_2)
                        await ctx.author.remove_roles(role_3)
                        await ctx.author.remove_roles(role_4)
                        await ctx.author.remove_roles(role_5)
                    elif lv >= 30:
                        await ctx.author.add_roles(role_1)
                        await ctx.author.remove_roles(role_2)
                        await ctx.author.remove_roles(role_3)
                        await ctx.author.remove_roles(role_4)
                        await ctx.author.remove_roles(role_5)
                    elif lv >= 20:
                        await ctx.author.add_roles(role_2)
                        await ctx.author.remove_roles(role_3)
                        await ctx.author.remove_roles(role_4)
                        await ctx.author.remove_roles(role_5)
                    elif lv >= 10:
                        await ctx.author.add_roles(role_3)
                        await ctx.author.remove_roles(role_4)
                        await ctx.author.remove_roles(role_5)
                    elif lv >= 5:
                        await ctx.author.add_roles(role_4)
                        await ctx.author.remove_roles(role_5)
                    else:
                        pass
                    embed = discord.Embed(colour = discord.Color.green(), title = 'покупка завершена', description = f"вы купили {exp} опыта за {exp} :moneybag:")
                    await ctx.send(embed = embed)
@buy_xp.error
async def buy_xp_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, укажи количество денег')

@bot.command(help = "выдает ежедневную награду")
async def daily(ctx):
    for guild in bot.guilds:
        if guild.id == config.your_guild_id:
            for row in cursor.execute(f"select * from work where id = {ctx.author.id};"):
                now = datetime.datetime.now()
                prev = datetime.datetime(row[1], row[2], row[3], row[4], row[5], row[6])
                delta = now - prev
                if (delta.days > 0):
                    year = now.year
                    month = now.month
                    day = now.day
                    hour = now.hour
                    minute = now.minute
                    second = now.second
                    for money in cursor.execute(f"select money from users where id = {ctx.author.id};"):
                        balance = money[0] + 100
                        cursor.execute(f'update users set money={balance} where id={ctx.author.id};')
                        conn.commit()
                        cursor.execute('update work set year={}, month={}, day={}, hour={}, minute={}, second={} where id={}'.format(year, month, day, hour, minute, day, ctx.author.id))
                        conn.commit()
                    embed = discord.Embed(colour = discord.Color.green(), description = "вы заработали 100 :moneybag:")
                    await ctx.send(embed = embed)
                else:
                    seconds = delta.seconds
                    hours = 24 - seconds // 3600 - 1
                    minutes = 60 - ((seconds % 3600) // 60)
                    if minutes < 10:
                        minutes = '0' + str(minutes)
                    seconds = 60 - seconds % 60
                    if seconds < 10:
                        seconds = '0' + str(seconds)
                    embed = discord.Embed(colour = discord.Color.red(), title = "ошибка", description = "попробуйте через {}:{}:{}".format(hours, minutes, seconds))
                    await ctx.send(embed = embed)
@bot.command(help = "выдает ежечасную награду")
async def hourly(ctx):
    for guild in bot.guilds:
        if guild.id == config.your_guild_id:
            for row in cursor.execute(f"select * from hour where id = {ctx.author.id};"):
                now = datetime.datetime.now()
                prev = datetime.datetime(row[1], row[2], row[3], row[4], row[5], row[6])
                delta = now - prev
                if (delta.seconds // 3600 > 0):
                    year = now.year
                    month = now.month
                    day = now.day
                    hour = now.hour
                    minute = now.minute
                    second = now.second
                    for money in cursor.execute(f"select money from users where id = {ctx.author.id};"):
                        balance = money[0] + 40
                        cursor.execute(f'update users set money={balance} where id={ctx.author.id};')
                        conn.commit()
                        cursor.execute('update hour set year={}, month={}, day={}, hour={}, minute={}, second={} where id = {}'.format(year, month, day, hour, minute, second, ctx.author.id))
                        conn.commit()
                    embed = discord.Embed(colour = discord.Color.green(), description = "вы заработали 40 :moneybag:")
                    await ctx.send(embed = embed)
                else:
                    seconds = delta.seconds
                    minutes = 60 - ((seconds % 3600) // 60) - 1
                    if minutes < 10:
                        minutes = '0' + str(minutes)
                    seconds = 60 - seconds % 60
                    if seconds < 10:
                        seconds = '0' + str(seconds)
                    embed = discord.Embed(colour = discord.Color.red(), title = "ошибка", description = "попробуйте через {}:{}".format(minutes, seconds))
                    await ctx.send(embed = embed)
            conn.commit()
@bot.command(help = "грабит указанного пользователя")
async def rob(ctx, member: discord.Member):
    for guild in bot.guilds:
        if guild.id == config.your_guild_id:
            for row in cursor.execute(f"select * from rob where id = {ctx.author.id};"):
                now = datetime.datetime.now()
                prev = datetime.datetime(row[1], row[2], row[3], row[4], row[5], row[6])
                delta = now - prev
                if (delta.seconds // 600 > 0):
                    year = now.year
                    month = now.month
                    day = now.day
                    hour = now.hour
                    minute = now.minute
                    second = now.second
                    cursor.execute('update rob set year={}, month={}, day={}, hour={}, minute={}, second={} where id = {}'.format(year, month, day, hour, minute, second, ctx.author.id))
                    conn.commit()
                    chance = random.randint(0, 100)
                    for money in cursor.execute(f"select money from users where id = {member.id};"):
                        if money[0] < 1:
                            await ctx.send(embed = discord.Embed(colour = discord.Color.red(), title = "ошибка", description = "пользователь без денег, лол"))
                            return
                        if chance > 50:
                            robamount = random.randint(1, money[0])
                            cursor.execute(f"update users set money = {money[0] - robamount} where id = {member.id};")
                            conn.commit()
                            for money in cursor.execute(f"select money from users where id = {ctx.author.id};"):
                                cursor.execute(f"update users set money = {money[0] + robamount} where id = {ctx.author.id};")
                                conn.commit()
                            embed = discord.Embed(colour = discord.Color.green(), title = ":white_check_mark: грабеж проведен успешно", description = f"вы ограбили пользователя {member.mention} на {robamount} :moneybag:")
                            await ctx.send(embed = embed)
                        else:
                            await ctx.send(embed = discord.Embed(colour = discord.Color.red(), description = "не удалось совершить кражу"))
                else:
                    seconds = delta.seconds
                    minutes = 10 - ((seconds % 600) // 60) - 1
                    minutes = '0' + str(minutes)
                    seconds = 60 - seconds % 60
                    if seconds < 10:
                        seconds = '0' + str(seconds)
                    embed = discord.Embed(colour = discord.Color.red(), title = "ошибка", description = "попробуйте через {}:{}".format(minutes, seconds))
                    await ctx.send(embed = embed)
            conn.commit()   

@bot.command(help = "позволяет положить указанную сумму денег на ваш банковский счет. максимум: 30% от всех ваших сбережений.")
async def deposit(ctx, amount: int):
    for guild in bot.guilds:
        if guild.id == config.your_guild_id:
            for row in cursor.execute(f'select money, bank from users where id = {ctx.author.id}'):
                banklimit = int((row[0] + row[1]) * 0.3)
                if amount + row[1] > banklimit:
                    await ctx.send(embed = discord.Embed(colour = discord.Color.red(), title = "ошибка", description = f"достигнут лимит сбережений на вашем банковском счету. лимит = {banklimit}"))
                else:
                    await ctx.send(embed = discord.Embed(colour = discord.Color.green(), title = "операция прошла успешно", description = f"вы успешно положили на ваш банковский счет {amount} :moneybag:.\nтекущий лимит составляет: {banklimit}"))
                    cursor.execute(f'update users set money = {row[0] - amount}, bank = {row[1] + amount} where id = {ctx.author.id}')
                    conn.commit()

@bot.command(help = "позволяет снять указанную сумму денег с вашего банковского счета.")
async def withdraw(ctx, amount: int):
    for guild in bot.guilds:
        if guild.id == config.your_guild_id:
            for row in cursor.execute(f'select money, bank from users where id = {ctx.author.id};'):
                if amount > row[1]:
                    await ctx.send(embed = discord.Embed(colour = discord.Color.red(), title = "ошибка", description = f"на вашем банковском счету недостаточно средств для снятия указанной суммы.\nтекущий баланс составляет: {row[1]} :moneybag:"))
                    return
                await ctx.send(embed = discord.Embed(colour = discord.Color.green(), title = "операция прошла успешно", description = f"вы успешно сняли {amount} :moneybag:\nостаток на счету: {row[1] - amount} :moneybag:"))
                cursor.execute(f'update users set money = {row[0] + amount}, bank = {row[1] - amount} where id = {ctx.author.id}')
                conn.commit()

@bot.command(help = "позволяет перевести указанную сумму денег указанному пользователю")
async def transfer(ctx, member: discord.Member, amount: int, *, message = None):
    for guild in bot.guilds:
        if guild.id == config.your_guild_id:
            for row in cursor.execute(f"select money from users where id = {ctx.author.id}"):
                if row[0] < amount:
                    await ctx.send(embed = discord.Embed(colour = discord.Color.red(), title = "ошибка", description = f"недостаточно средств на вашем балансе.\nтекущий баланс составляет: {row[0]} :moneybag:"))
                    return
                first_balance = row[0]
            cursor.execute(f"update users set money = {first_balance - amount} where id = {ctx.author.id}")
            conn.commit()
            for row in cursor.execute(f"select money from users where id = {member.id}"):
                second_balance = row[0]
            cursor.execute(f"update users set money = {second_balance + amount} where id = {member.id}")
            conn.commit()
            await ctx.send(embed = discord.Embed(colour = discord.Color.green(), title = ":white_check_mark: перевод проведен успешно", description = f"вы перевели пользователю {member.mention} {amount} :moneybag:"))

@bot.command(help = "отображает карточку пользователя", aliases = ['lvl', 'account'])
async def profile(ctx, member: discord.Member = None):
    for guild in bot.guilds:
        if guild.id == config.your_guild_id:
            print(ctx.author.id)
            if member == None:
                for row in cursor.execute(f"SELECT nickname, money, bank, lvl, xp FROM users where id={ctx.author.id};"):
                    embed = discord.Embed(title = f"ваш профиль", 
                    description = f"никнейм: {row[0]}\nбаланс: {row[1]}:moneybag:\nсумма в банке: {row[2]}:moneybag:\nуровень: {row[3]}\nпрогресс уровня: {row[4]} / {(row[3]) ** 2 * 100}", 
                    colour = discord.Color.dark_purple())
                    embed.set_image(url = ctx.author.avatar_url)
                    await ctx.send(embed = embed)
            else:
                for row in cursor.execute(f"SELECT nickname, money, bank, lvl, xp FROM users where id={member.id};"):
                    embed = discord.Embed(title = f"профиль {row[0]}", 
                    description = f"никнейм: {row[0]}\nбаланс: {row[1]}:moneybag:\nсумма в банке: {row[2]}:moneybag:\nуровень: {row[3]}\nпрогресс уровня: {row[4]} / {(row[3]) ** 2 * 100}", 
                    colour = discord.Color.dark_purple())
                    embed.set_image(url = member.avatar_url)
                    await ctx.send(embed = embed)

bot.run(config.settings['token'], bot = True)