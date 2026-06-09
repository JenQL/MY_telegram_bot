
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from results_4d import get_4d_results
import os

# Replace with your BotFather token
TOKEN = os.getenv("Tele_Token")


# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Use /results to check the latest 4D results.")


async def results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if context.args:
            date_str = context.args[0]  # user provides /results YYYY-MM-DD
            data = get_4d_results(date_str)
        else:
            data = get_4d_results()
        await update.message.reply_text(f"4D Results:\n{data}")
    except Exception as e:
        await update.message.reply_text(f"Error fetching results: {e}")


def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("results", results))

    application.run_polling()

if __name__ == "__main__":
    main()





