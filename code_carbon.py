import os
import uuid
import requests
from telegram import ChatAction, Update, Chat
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler, Filters, MessageHandler

CODE_INPUT = 0

CARBON_API = os.getenv("CARBON_API")

def code_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Envíame tu código y te devolveré una imagen con la sintaxis resaltada.'
    )

    return CODE_INPUT


def code_input_text(update: Update, context: CallbackContext):
    code = text = update.message.text

    api_url = f"{CARBON_API}/"

    response = requests.post(api_url, json=dict(code=code, language="dart"))

    if (response.status_code == 200):
        filename = save_file(response.content)

        send_file(filename, update.message.chat)

        os.unlink(filename)
    else:
        update.message.reply_text(
            "Ocurrión un error al generar la imagen para el código")

    return ConversationHandler.END


def save_file(file: bytes):
    filename = f"{str(uuid.uuid1())}.png"

    open(filename, 'wb').write(file)

    return filename


def send_file(filename: str, chat: Chat):
    chat.send_action(action=ChatAction.UPLOAD_PHOTO, timeout=None)

    chat.send_photo(
        photo=open(filename, 'rb')
    )


code_command = ConversationHandler(
    entry_points=[
        CommandHandler("code", code_handler)
    ],
    states={
        CODE_INPUT: [
            MessageHandler(Filters.text, code_input_text)
        ],
    },
    fallbacks=[]
)
