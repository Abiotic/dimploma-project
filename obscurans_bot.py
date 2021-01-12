import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
import wikipedia
import wikipediaapi
import settings
import time
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
	user_text = update.message.text
	comparison_res = input_comparison(user_text)
	if comparison_res == None:
		update.message.reply_text('Попробуйте еще раз')
	#print(f'kek + {comparison_res}')
	else:
		answer = wiki_search(comparison_res)
		#print(answer)
		update.message.reply_text(answer)


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
	#threshold = 2
	with open('conspiracy_obscurans_db.txt','r', encoding='utf-8') as f:
		for line in f:
			line = line.lower().strip()
			dld = jf.damerau_levenshtein_distance(text,line)
			if dld < 0.15*len(line) or dld <= 2:
				return line 
	return None



def wiki_search(theory):
	key_word = 'Критика'
	wikipedia.set_lang("ru")
	w_page = wikipedia.page(theory)
	for sec in w_page.sections:
		if key_word in sec:
			return f'бла бла (придумать текст) \n{w_page.section(sec)}'
		else:
			return f'Не смог найти для тебя критику, поэтому держи:\n{w_page.summary}'



if __name__ == "__main__":
	main()
