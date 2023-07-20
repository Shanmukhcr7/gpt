import os
import requests
from PIL import Image
import pytesseract
import telegram
from telegram.ext import Updater, MessageHandler, Filters
import openai

# Set up the Telegram Bot API token
TELEGRAM_TOKEN = '6213526480:AAEXHsRPWe6Hv1KeQAhVZr2ChEh0w_iG_qk'

# Set up the OpenAI API credentials
OPENAI_API_KEY = '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'

# Initialize the Telegram bot
bot = telegram.Bot(token=TELEGRAM_TOKEN)

# Set up the OpenAI API client
openai.api_key = OPENAI_API_KEY

# Set up the image processing library (pytesseract and PIL)


def process_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text.strip()


def send_message(chat_id, text):
    bot.send_message(chat_id=chat_id, text=text)


def handle_message(update, context):
    if update.message.photo:
        # Handle image messages
        photo_file_id = update.message.photo[-1].file_id
        photo_file = context.bot.get_file(photo_file_id)
        photo_path = 'temp.jpg'
        photo_file.download(photo_path)
        extracted_text = process_image(photo_path)
        chatgpt_response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=extracted_text,
            max_tokens=50
        )
        response_text = chatgpt_response.choices[0].text.strip()
        send_message(update.message.chat_id, response_text)
        os.remove(photo_path)
    elif update.message.text:
        # Handle text messages
        text_message = update.message.text
        chatgpt_response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=text_message,
            max_tokens=50
        )
        response_text = chatgpt_response.choices[0].text.strip()
        send_message(update.message.chat_id, response_text)


def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text | Filters.photo, handle_message))
    updater.start_polling()
    print("Bot started!")
    updater.idle()


if __name__ == '__main__':
    main()