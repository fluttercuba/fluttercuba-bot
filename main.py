from discord import Webhook, RequestsWebhookAdapter
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import MessageEntity
import os
from dotenv import load_dotenv
load_dotenv()

<<<<<<< HEAD
# Variables
api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
COUNT_PER_PAGE_DEVTO = 2
INTERVAL_BY_HOURS = 1800  # 30m
# # clients
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


@client_telegram.on(events.NewMessage(chats=[1486641070], pattern="(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-&?=%.]+"))
async def handler(event):
    message = event.original_update.to_dict()
    message_text = message.get("message").get("message")
    channel = bot.get_channel(816098689206190080)
    await channel.send(message_text)


=======
>>>>>>> 427d2787a1468b3ba7298163ee757286801a74ad
def start(update, context):
    update.message.reply_text("Hey Flutter Cuba ")
def share_url_callback(update, context):
    webhook = Webhook.from_url(
        url=os.getenv("DISCORD_WEBHOOK"),
        adapter=RequestsWebhookAdapter(),
    )
    webhook.send(update.message.text, username='fluttercuba-bot')
    update.message.reply_text("compartiendo url...")
def main():
    """Start the bot."""
    updater = Updater(os.getenv("TELEGRAM_TOKEN"))
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    url_handler = MessageHandler(
    Filters.text & (Filters.entity(MessageEntity.URL) |
                    Filters.entity(MessageEntity.TEXT_LINK)),
    share_url_callback)
    dp.add_handler(url_handler)
    updater.start_webhook(
        listen="0.0.0.0",
        port=os.getenv("PORT"),
        url_path=os.getenv("TELEGRAM_TOKEN"),
    )
    updater.bot.set_webhook(
        "https://fluttercubabot.herokuapp.com/" + os.getenv("TELEGRAM_TOKEN"),
    )

    updater.idle()


if __name__ == '__main__':
    main()
