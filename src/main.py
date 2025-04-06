import logging
import os
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters, Application
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),  # Console
        logging.FileHandler("../bot.log")  # File
    ]
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN not found in environment!")

BOT_USERNAME = os.getenv("BOT_USERNAME")  # You can use this if needed for group parsing

# In-memory user data store (should be replaced with a database for scalability)
user_data = {}

def get_user_data(user_id):
    if user_id not in user_data:
        user_data[user_id] = {
            'balance': 0.0,
            'debt': 0.0,
            'max_debt': 100.0  # arbitrary default
        }
    return user_data[user_id]

# Commands
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🛠 *Available Commands:*\n\n"
        "/help – Show this help message\n"
        "/info – Show your balance, current debt, and max debt\n"
        "/balance – Show only your balance\n"
        "/debt – Show only your debt\n"
        "/maxdebt – Show only your max possible debt\n"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    data = get_user_data(user_id)

    message = (
        f"💰 Balance: {data['balance']:.2f} zł\n"
        f"📉 Current Debt: {data['debt']:.2f} zł\n"
        f"🚨 Max Possible Debt: {data['max_debt']:.2f} zł"
    )

    await update.message.reply_text(message)

async def balance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = get_user_data(user_id)
    await update.message.reply_text(
        f"💰 Balance: {data['balance']:.2f} PLN"
    )

async def debt_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = get_user_data(user_id)
    await update.message.reply_text(
        f"💸 Current Debt: {data['debt']:.2f} PLN"
    )

async def maxdebt_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = get_user_data(user_id)
    await update.message.reply_text(
        f"📉 Max Possible Debt: {data['max_debt']:.2f} PLN"
    )

# Responses
def handle_response(txt: str) -> str:
    lowered_txt: str = txt.lower()
    if 'hello' in lowered_txt:
        return 'Hi there!'
    if 'mistrz' in lowered_txt:
        return 'Aurel jest mistrzem!'
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
    logger.error(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    logger.info("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('info', info_command))
    app.add_handler(CommandHandler('balance', balance_command))
    app.add_handler(CommandHandler('debt', debt_command))
    app.add_handler(CommandHandler('maxdebt', maxdebt_command))

    # Add message handler for user responses
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polling
    logger.info("Polling...")
    app.run_polling(poll_interval=1)
