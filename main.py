from discord import Webhook, RequestsWebhookAdapter
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import MessageEntity
import os
import re
from dotenv import load_dotenv
load_dotenv()

REGEX_URL = ur"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"


def start(update, context):
    update.message.reply_text("Hey Flutter Cuba ")


def socials(update, context):
    update.message.reply_text(
        """
        github: https://github.com/fluttercuba
        discord: https://discord.gg/CtdVKf5w
        telegram: https://t.me/fluttercuba
        twitter: https://twitter.com/flutterCuba
        """
    )


def share_url_callback(update, context):
    text_with_url = update.message.text

    matches_urls = re.findall(REGEX_URL, text_with_url)
    for url in matches_urls:
        webhook = Webhook.from_url(
            url=os.getenv("DISCORD_WEBHOOK"),
            adapter=RequestsWebhookAdapter(),
        )
        webhook.send(url, username='fluttercuba-bot')
        update.message.reply_text("compartiendo url...")


def main():
    """Start the bot."""
    updater = Updater(os.getenv("TELEGRAM_TOKEN"))
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("info", socials))
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
