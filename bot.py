from utils.compiler import encrypt as encrypt_text, decrypt as decrypt_text, base64
from dotenv import dotenv_values
from datetime import datetime
from telegram.ext import *
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

HELP = """Dear NAME,
welcome to winger bot. You can see all the commands below

Commands:
    /help       display the help message
    /text       Encrypt/Decrypt text
    /file       Encrypt/Decrypt file
"""

ERROR = "Command or text is not define, enter the /help command to see more " \
        "details."

TEXT_ENCRYPTION = {"status": False, "method": None}
FILE_ENCRYPTION = {"status": False, "method": None}

def consoleLog(update):
    print(f"{datetime.now()}: {update.message.chat} -> {update.message.text}")

def start_command(update, context):
    chat_id = update.effective_chat.id
    first_name = update.message.chat["first_name"]
    update.message.reply_text(HELP.replace("NAME", first_name))
    consoleLog(update)

def text_command(update, text):
    global TEXT_ENCRYPTION, FILE_ENCRYPTION

    try:
        answer = eval(f"{TEXT_ENCRYPTION['method']}_text(text)")
        update.message.reply_text(answer)

    except base64.binascii.Error:
        update.message.reply_text(f"Can not decrypt {text}")

    TEXT_ENCRYPTION["status"] = False
    TEXT_ENCRYPTION["method"] = None

def toggle_choose_action_for_text(update, context):
    # reset the values
    global TEXT_ENCRYPTION
    TEXT_ENCRYPTION["status"] = True
    TEXT_ENCRYPTION["method"] = None

    reply_markup = ReplyKeyboardMarkup([["Encrypt", "Decrypt"]])
    update.message.reply_text("Choose the action", reply_markup=reply_markup)
    consoleLog(update)

def toggle_choose_action_for_file(update, context):
    # reset the values
    global FILE_ENCRYPTION
    FILE_ENCRYPTION["status"] = True
    FILE_ENCRYPTION["method"] = None

    reply_markup = ReplyKeyboardMarkup([["Encrypt", "Decrypt"]])
    update.message.reply_text("Choose the action", reply_markup=reply_markup)
    consoleLog(update)

def handle_message(update, context):
    text = update.message.text

    if text in ("Encrypt", "Decrypt"):
        if TEXT_ENCRYPTION["status"]:
            TEXT_ENCRYPTION["method"] = text.lower()
            update.message.reply_text("Enter the text that you want to " + \
            text.lower(), reply_markup=ReplyKeyboardRemove(remove_keyboard=True))

        elif FILE_ENCRYPTION["status"]:
            FILE_ENCRYPTION["method"] = text.lower()
            update.message.reply_text("Enter the file that you want to " + \
            text.lower(), reply_markup=ReplyKeyboardRemove(remove_keyboard=True))

        else:
            update.message.reply_text(ERROR)

    elif TEXT_ENCRYPTION["status"] and TEXT_ENCRYPTION["method"]:
        text_command(update, text)

    elif FILE_ENCRYPTION["status"] and FILE_ENCRYPTION["method"]:
        # TODO: complete this part and finish the program
        pass

    else:
        update.message.reply_text(ERROR)

    consoleLog(update)


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
    dp.add_handler(CommandHandler("help", start_command))
    dp.add_handler(CommandHandler("text", toggle_choose_action_for_text))
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    print("bot is running...")
    updater.start_polling()