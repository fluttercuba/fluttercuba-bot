import re
import os
import discord
import requests
from telethon import TelegramClient, events, sync
from discord.ext import commands
# from dotenv import load_dotenv

# load_dotenv()

# Variables
api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
COUNT_PER_PAGE_DEVTO = 1

# clients
bot = commands.Bot(command_prefix='!')

client_telegram = TelegramClient(
    os.getenv('TELEGRAM_APP_NAME'),
    api_id,
    api_hash,
)
client_telegram.start()

# Discord logic


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hola {member.name}, Bienvenido a flutterCuba Discord server! teclea !help para saber los comandos'
    )


@bot.command(help="Muestra las redes sociales")
async def info(ctx):
    await ctx.send("""
    github: https://github.com/fluttercuba
    discord: https://discord.gg/CtdVKf5w 
    telegram: https://t.me/fluttercuba
    twitter: https://twitter.com/flutterCuba
    """)


@bot.command(help="!articles <tagname> Muestra los ultimos 2 articluos https://dev.to")
async def articles(ctx, arg):
    r = requests.get(
        f"https://dev.to/api/articles?tag={arg}&per_page={COUNT_PER_PAGE_DEVTO}",
    )
    value = list(map(
        lambda article: {
            "title": article.get('title'),
            "description": article.get('description'),
            "url": article.get('url'),
            "published_at": article.get('published_at'),
        }, r.json(),
    ))
    channel = bot.get_channel(817478457688719410)

    for article in value:
        embed = discord.Embed(
            title=article.get("title"),
            url=article.get("url"),
            description=article.get("description"),
            color=0x109319,
        )

        await channel.send(embed=embed)


# telegram handler
@client_telegram.on(events.NewMessage(chats=[1486641070], pattern="(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-&?=%.]+"))
async def handler(event):
    message = event.original_update.to_dict()
    message_text = message.get("message").get("message")
    channel = bot.get_channel(816098689206190080)
    await channel.send(message_text)


bot.run(os.getenv('DISCORD_TOKEN'))
