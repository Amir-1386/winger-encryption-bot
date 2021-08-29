from utils.compiler import encrypt as encrypt_text, decrypt as decrypt_text, base64
from dotenv import dotenv_values
from datetime import datetime
from telegram.ext import *
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import os

START = """Dear NAME,
welcome to winger bot. You can see all the commands below

Commands:
    /help       display the help message
    /text       Encrypt/Decrypt text
"""

HELP = """
Commands:
    /help       display the help message
    /text       Encrypt/Decrypt text
"""

ERROR = "Command or text is not define, enter the /help command to see more " \
        "details."

TEXT_ENCRYPTION = {}

def consoleLog(update, content):
    print(f"{datetime.now()}: {update.message.chat} -> {content}")

def start_command(update, context):
    global TEXT_ENCRYPTION
    
    TEXT_ENCRYPTION[update.message.chat["id"]] = {"status": False, "method": None}
    
    chat_id = update.effective_chat.id
    first_name = update.message.chat["first_name"]
    update.message.reply_text(START.replace("NAME", first_name))
    
    consoleLog(update, update.message.text)

def help_command(update, context):
    global TEXT_ENCRYPTION
    
    TEXT_ENCRYPTION[update.message.chat["id"]] = {"status": False, "method": None}
    
    chat_id = update.effective_chat.id
    first_name = update.message.chat["first_name"]
    update.message.reply_text(HELP)
    
    consoleLog(update, update.message.text)

def text_command(update, text):
    global TEXT_ENCRYPTION

    try:
        if TEXT_ENCRYPTION[update.message.chat['id']]['method'] == 'encrypt':
            answer = encrypt_text(text)
        elif TEXT_ENCRYPTION[update.message.chat['id']]['method'] == 'decrypt':
            answer = decrypt_text(text)
    except:
        update.message.reply_text(f"Can not {TEXT_ENCRYPTION[update.message.chat['id']]['method']} {text}")
    else:
        update.message.reply_text(answer)

    TEXT_ENCRYPTION[update.message.chat["id"]] = {"status": False, "method": None}

def toggle_choose_action_for_text(update, context):
    # reset the values
    global TEXT_ENCRYPTION
    TEXT_ENCRYPTION[update.message.chat["id"]] = {"status": True, "method": None}

    reply_markup = ReplyKeyboardMarkup([["/encrypt", "/decrypt"]])
    update.message.reply_text("Choose the action", reply_markup=reply_markup)

    consoleLog(update, update.message.text)

def encrypt_mode(update, context):
    if TEXT_ENCRYPTION[update.message.chat["id"]]["status"]:
        TEXT_ENCRYPTION[update.message.chat["id"]]["method"] = "encrypt"
        update.message.reply_text("Enter the text that you want to " + \
        "encrypt", reply_markup=ReplyKeyboardRemove(remove_keyboard=True))

    else:
        update.message.reply_text(ERROR)

def decrypt_mode(update, context):
    if TEXT_ENCRYPTION[update.message.chat["id"]]["status"]:
        TEXT_ENCRYPTION[update.message.chat["id"]]["method"] = "decrypt"
        update.message.reply_text("Enter the text that you want to " + \
        "decrypt", reply_markup=ReplyKeyboardRemove(remove_keyboard=True))

    else:
        update.message.reply_text(ERROR)

def handle_message_text(update, context):
    
    if TEXT_ENCRYPTION[update.message.chat["id"]]["status"] and TEXT_ENCRYPTION[update.message.chat["id"]]["method"]:
        text = update.message.text
        
        text_command(update, text)
        help_command(update, context)
    
    else:
        update.message.reply_text(ERROR)

    consoleLog(update, update.message.text)


if __name__ == "__main__":
    environment_varables = dotenv_values(".env")

    # raise error for not existing .env file
    if "API_TOKEN" not in environment_varables.keys():
        raise FileNotFoundError("You have to create a file and name it '.env'" \
                                    + " then pass in your API_TOKEN")

    API_TOKEN = environment_varables["API_TOKEN"]

    updater = Updater(API_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("text", toggle_choose_action_for_text))
    dp.add_handler(CommandHandler("encrypt", encrypt_mode))
    dp.add_handler(CommandHandler("decrypt", decrypt_mode))
    dp.add_handler(MessageHandler(Filters.text, handle_message_text))

    print("bot is running...")
    updater.start_polling()
