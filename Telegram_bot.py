
from telegram.ext import Updater, CommandHandler
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from results_4d import get_4d_results
import os

# Replace with your BotFather token
TOKEN = os.getenv("Tele_Token")


# Command: /start
def start(update, context):
    update.message.reply_text("Welcome! Use /results to check the latest 4D results.")


def results(update, context):
    try:
        if context.args:
            date_str = context.args[0]  # user provides /results YYYY-MM-DD
            data = get_4d_results(date_str)
        else:
            data = get_4d_results()
        update.message.reply_text(f"4D Results:\n{data}")
    except Exception as e:
        update.message.reply_text(f"Error fetching results: {e}")


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("results", results))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()





