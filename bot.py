from utils.compiler import encrypt, decrypt
from dotenv import dotenv_values
from datetime import datetime
from telegram.ext import *

HELP = """Dear NAME,
welcome to winger bot. You can see all the commands below

Commands:
    /help       display the help message
    /text       encrypt text
    /file       encrypt file
"""

def consoleLog(update):
    print(f"{datetime.now()}: {update.message.chat} -> {update.message.text}")

def start_command(update, context):
    first_name = update.message.chat["first_name"]
    update.message.reply_text(HELP.replace("NAME", first_name))
    consoleLog(update)


if __name__ == "__main__":
    environment_varables = dotenv_values(".env")

    # raise error for not existing .env file
    if "API_TOKEN" not in environment_varables.keys():
        raise FileNotFoundError("You have to create a file and name it '.env' then pass in your API_TOKEN")

    API_TOKEN = environment_varables["API_TOKEN"]

    updater = Updater(API_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", start_command))

    print("bot is running...")
    updater.start_polling()