from discord import Webhook, RequestsWebhookAdapter
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import MessageEntity
import os
from dotenv import load_dotenv
load_dotenv()


def start(update, context):
    update.message.reply_text("Hey Flutter Cuba ")


def info(update, context):
    update.message.reply_text(
        """
        github: https://github.com/fluttercuba
        discord: https://discord.gg/CtdVKf5w
        telegram: https://t.me/fluttercuba
        twitter: https://twitter.com/flutterCuba
        """
    )


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
    dp.add_handler(CommandHandler("info", info))
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
