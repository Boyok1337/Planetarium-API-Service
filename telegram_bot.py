import logging
import os
import time

import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext, \
    ConversationHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

user_tokens = {}
EMAIL = range(1)


async def start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text('Hello! Please enter your email address.')
    return EMAIL


async def handle_email(update: Update, context: CallbackContext) -> int:
    email = update.message.text
    context.user_data['email'] = email
    await update.message.reply_text('Sending request to the server...')

    return await send_email_request(update, context)


async def send_email_request(update: Update, context: CallbackContext) -> int:
    email = context.user_data['email']
    url = 'http://planetarium:8000/api/planetarium/tickets-by-email/'  # Use the service name as the hostname
    data = {'email': email}

    max_retries = 5
    retry_delay = 5

    for attempt in range(max_retries):
        try:
            response = requests.post(url, data=data)

            if response.status_code in range(200, 300):
                response_data = response.json()
                if response_data.get('status') == 'success':
                    tickets = response_data.get('data', [])
                    html_response = "<b>API Response:</b>\n"
                    for ticket in tickets:
                        html_response += (f"ID: {ticket['id']}, "
                                          f"Row: {ticket['row']}, "
                                          f"Seat: {ticket['seat']}, "
                                          f"Show Session: {ticket['show_session_id']}, "
                                          f"Reservation: {ticket['reservation_id']}\n")
                    await update.message.reply_text(html_response, parse_mode='HTML')
                else:
                    await update.message.reply_text(f'Error: {response_data.get("message", "Unknown error")}')
            else:
                await update.message.reply_text(
                    f'Error occurred while making a request to the API: {response.status_code} {response.text}')
            break
        except Exception as e:
            if attempt < max_retries - 1:
                await update.message.reply_text(f'Error occurred while making a request to the API: {str(e)}. Retrying...')
                time.sleep(retry_delay)
            else:
                await update.message.reply_text(f'Error occurred while making a request to the API: {str(e)}. No more retries left.')
                break

    await update.message.reply_text('Enter a new email address or /start to restart.')
    return EMAIL


def main() -> None:
    token = os.environ.get('TELEGRAM_TOKEN')

    application = ApplicationBuilder().token(token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_email)],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
