import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, Application
import os

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),  # Console
        logging.FileHandler("bot.log")  # File
    ]
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN not found in environment!")

BOT_USERNAME = os.getenv("BOT_USERNAME")

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Thanks for reaching me! I ma a PlusEV bot')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I ma a PlusEV bot! Please type something so I can respond')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command!')

# Responses
def handle_response(txt: str) -> str:
    lowered_txt: str = txt.lower()
    if 'hello' in lowered_txt:
        return 'Hi there!'
    if 'mistrz' in lowered_txt:
        return 'Aurel jest mistrzem!'
    if 'a grucha?' in lowered_txt:
        return 'nie znam typa, pewnie ciota...'
    return 'I do not understand what do you want...'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot: ', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    logger.info("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    # Cmmands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    logger.error("Some error message")
    app.add_error_handler(error)

    # Polls
    logger.info("Polling...")
    app.run_polling(poll_interval=0.1)