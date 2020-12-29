import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup

import settings

logging.basicConfig(filename='bot.log', level=logging.INFO)

#PROXY 
"""
PROXY= {'proxy_url': settings.PROXY_URL,
		'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}
"""


def greet_user(update, context):
	print("Вызван /start")
	update.message.reply_text(
		f"Привет! Сюда ты можешь писать безумные, антинаучные теории, а я попытаюсь рассказать, что в них не так. Или нет...",
		reply_markup=main_keyboard()
		)


def talk_to_me(update,context):
	text = update.message.text
	print(text)
	update.message.reply_text("Надо подумать...")

def main():
	mybot = Updater(settings.API_KEY,use_context = True)

	dp = mybot.dispatcher
	dp.add_handler(CommandHandler("start",greet_user))
	#dp.add_handler(MessageHandler(Filters.regex('^(начнем)$'), greet_user))
	dp.add_handler(MessageHandler(Filters.text, talk_to_me))

	logging.info("Bot was launched")
	mybot.start_polling()
	mybot.idle()


def main_keyboard():
	return ReplyKeyboardMarkup([['/start']])


if __name__ == "__main__":
	
	main()
