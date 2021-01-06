import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
import wikipedia
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
	user_text = update.message.text
	comparison_res = input_comparison(user_text)
	#print(comparison_res) check2
	theory_summary = wiki_search(comparison_res)
	update.message.reply_text(theory_summary) 


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

def input_comparison(text):
	text = text.lower()

	with open('conspiracy_obscurans_db.txt','r', encoding='utf-8') as f:
		for line in f:
			line = line.lower()
			if text in line:
				#print(line) check
				return line

def wiki_search(theory):
	wikipedia.set_lang("ru")
	wiki_page = wikipedia.page(theory)
	return wiki_page.summary



if __name__ == "__main__":
	
	main()
