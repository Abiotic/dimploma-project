import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
import wikipedia
import settings
import jellyfish as jf

#wikipediaapi.log.setLevel(level=wikipediaapi.logging.DEBUG)
logging.basicConfig(filename='bot.log', level=logging.INFO)

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
	user_input = update.message.text
	comparison_res = input_comparison(user_input)
	if comparison_res == None:
		update.message.reply_text('Попробуйте еще раз')
	else:
		answer = wiki_search(comparison_res)
		update.message.reply_text(answer)


def main():
	mybot = Updater(settings.API_KEY,use_context = True)
	dp = mybot.dispatcher
	dp.add_handler(CommandHandler("start",greet_user))
	dp.add_handler(MessageHandler(Filters.text, talk_to_me))
	logging.info("Bot was launched")
	mybot.start_polling()
	mybot.idle()


def main_keyboard():
	return ReplyKeyboardMarkup([['/start']])

def input_comparison(user_input):
	user_input = user_input.lower()

	with open(settings.THEORY_DB,'r', encoding='utf-8') as f:
		for line in f:
			line = line.lower().strip()
			
			if is_misprint_below_threshold(user_input, line):
				return line 
	return None

def is_misprint_below_threshold (user_input, db_line):
	allowed_misprints = 2
	misprint_threshold = 0.15
	distance = jf.damerau_levenshtein_distance(user_input,db_line)
	return distance < misprint_threshold*len(db_line) or distance <= allowed_misprints


def wiki_search(theory):
	key_word = 'Критика'
	wikipedia.set_lang("ru")
	w_page = wikipedia.page(theory)
	for sec in w_page.sections:
		if key_word in sec:
			return f'Критика: \n{w_page.section(sec)}'

	return f'Не смог найти для тебя критику, поэтому держи описание:\n{w_page.summary}'



if __name__ == "__main__":
	main()
