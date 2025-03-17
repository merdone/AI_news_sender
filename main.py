import telebot
from telebot import types
from dotenv import load_dotenv
from parse import *
from translate import *
from gpt import get_gpt_answer, sample_translate, sample_retell
import os

load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))

editions = ["BILD", "Spiegel", "CNN", "BBC", "The Daily Telegraph"]
editions_url = ["bild", "spiegel", "cnn", "bbc", "telegraph"]

func_list = [parse_list_bild, parse_list_spiegel, parse_list_cnn, parse_list_bbc, parse_list_telegraph]
func_text = [parse_text_bild, parse_text_spiegel, parse_text_cnn, parse_text_bbc, parse_text_telegraph]

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(types.KeyboardButton("📜 Список джерел"),
           types.KeyboardButton("✉ Залишити відгук"))

first_choice = types.InlineKeyboardMarkup(row_width=1)
for temp in editions:
    first_choice.add(types.InlineKeyboardButton(text=temp, callback_data=temp))
first_choice.add(types.InlineKeyboardButton(text="Переклад за посиланням", callback_data="work_url"))

third_choice = types.InlineKeyboardMarkup(row_width=2)
third_choice.add(types.InlineKeyboardButton(text="Перекласти AI", callback_data="translate_ai"),
                 types.InlineKeyboardButton(text="Перекласти Google", callback_data="translate_google"),
                 types.InlineKeyboardButton(text="Скоротити", callback_data="make_short"))

third_choice_ai = types.InlineKeyboardMarkup(row_width=2)
third_choice_ai.add(types.InlineKeyboardButton(text="Перекласти Google", callback_data="translate_google"),
                    types.InlineKeyboardButton(text="Скоротити", callback_data="make_short"),
                    types.InlineKeyboardButton(text="Завершити роботу", callback_data="cancel"))

third_choice_gl = types.InlineKeyboardMarkup(row_width=2)
third_choice_gl.add(types.InlineKeyboardButton(text="Перекласти AI", callback_data="translate_ai"),
                    types.InlineKeyboardButton(text="Скоротити", callback_data="make_short"),
                    types.InlineKeyboardButton(text="Завершити роботу", callback_data="cancel"))

third_choice_sh = types.InlineKeyboardMarkup(row_width=2)
third_choice_sh.add(types.InlineKeyboardButton(text="Перекласти AI", callback_data="translate_ai"),
                    types.InlineKeyboardButton(text="Перекласти Google", callback_data="make_short"),
                    types.InlineKeyboardButton(text="Завершити роботу", callback_data="cancel"))


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAECo79ljVIJMGtC055ZKwT24S50L81lHAAC2A8AAkjyYEsV-8TaeHRrmDME")
    bot.send_message(message.chat.id,
                     "Для того, щоб почати роботу, оберіть статтю, натиснувши на кнопку знизу 👇",
                     reply_markup=markup)


@bot.message_handler(content_types="text")
def start_news(message):
    global start_message
    if message.text == "📜 Список джерел":
        start_message = bot.send_message(message.chat.id, "<b>Оберіть джерело, з якого брати статтю:</b>", reply_markup=first_choice,
                         parse_mode="html")
    elif message.text == "✉ Залишити відгук":
        feedback_message = bot.send_message(message.chat.id, "Будь ласка, залиште свій відгук:")
        bot.register_next_step_handler(feedback_message, input_feedback)


def input_feedback(message):
    file = open('feedback.txt', 'a')
    try:
        file.write(message.text + "\n")
    except:
        pass
    file.close()
    bot.send_message(message.chat.id, "Дякую за відгук! Гарного дня 😺")
    start_news(message)


def input_url(message):
    global previous_message
    global message_text
    try:
        if message.text.split("/")[2].split(".")[1] in editions_url:
            message_text = func_text[editions_url.index(message.text.split("/")[2].split(".")[1])]("", message.text)
            previous_message = bot.send_message(message.chat.id, message_text, reply_markup=third_choice)
        else:
            bot.send_message(message.chat.id, "Некоректне посилання. Спробуйте ще раз.")
            start_news(message)
    except:
        bot.send_message(message.chat.id, "Не можу відправити вам цю статтю, через ліміт слів у повідомленні в "
                                          "телеграмі.Спробуйте іншу статтю.")
        start_news(message)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global message_text
    global previous_message
    try:
        if call.data in editions:
            text = ""
            for i in range(len(list(func_list[editions.index(call.data)]().keys()))):
                text += f"{i + 1} - {translate_text(list(func_list[editions.index(call.data)]().keys())[i])}\n\n"
            second_choice = types.InlineKeyboardMarkup(row_width=5)
            for temp in range(len(func_list[editions.index(call.data)]())):
                second_choice.add(types.InlineKeyboardButton(text=str(temp + 1),
                                                             callback_data=f"request.{temp}.{editions[editions.index(call.data)]}"))
            bot.delete_message(call.message.chat.id, start_message.message_id)
            previous_message = bot.send_message(call.message.chat.id, f"<b>Оберіть одну з статей:</b>\n\n {text}",
                                                reply_markup=second_choice, parse_mode="html")
        if call.data == "work_url":
            message_url = bot.send_message(call.message.chat.id, "Введіть посилання, з якого брату статтю: \n "
                                                                 "Приймаються посилання: \n <b>Bild, Spiegel, CNN, "
                                                                 "BBC, The Daily Telegraph</b>", parse_mode="html")
            bot.register_next_step_handler(message_url, input_url)

        if call.data.startswith("request"):
            first_part = call.data.split(".")
            second_part = editions.index(call.data.split(".")[-1])
            message_text = func_text[second_part](list(func_list[second_part]().keys())[int(first_part[1])], "")
            bot.delete_message(call.message.chat.id, previous_message.message_id)
            previous_message = bot.send_message(call.message.chat.id, message_text, reply_markup=third_choice)
        if call.data == "cancel":
            bot.delete_message(call.message.chat.id, previous_message.message_id)
            bot.send_message(call.message.chat.id, "Дякую за те що користуєтесь мною. Гарного Вам дня!")
            start_news(call.message)
        if "translate" in call.data:
            if "ai" in call.data:
                bot.delete_message(call.message.chat.id, previous_message.message_id)
                waiting_message = bot.send_sticker(call.message.chat.id,
                                                   "CAACAgIAAxkBAAECo-VljVxoT8_jubOyMcU6LlPW2YKbmwACIwADKA9qFCdRJeeMIKQGMwQ")
                previous_message = bot.send_message(call.message.chat.id,
                                                    get_gpt_answer(message_text, sample_translate),
                                                    reply_markup=third_choice_ai)
                bot.delete_message(call.message.chat.id, waiting_message.message_id)
            else:
                bot.delete_message(call.message.chat.id, previous_message.message_id)
                previous_message = bot.send_message(call.message.chat.id, translate_text(message_text),
                                                    reply_markup=third_choice_gl)
        if call.data == "make_short":
            bot.delete_message(call.message.chat.id, previous_message.message_id)
            waiting_message = bot.send_sticker(call.message.chat.id,
                                               "CAACAgIAAxkBAAECo-VljVxoT8_jubOyMcU6LlPW2YKbmwACIwADKA9qFCdRJeeMIKQGMwQ")
            previous_message = bot.send_message(call.message.chat.id, get_gpt_answer(message_text, sample_retell),
                                                reply_markup=third_choice_sh)
            bot.delete_message(call.message.chat.id, waiting_message.message_id)


    except:
        bot.send_message(call.message.chat.id, "Вибачте, сталась помилка, оберіть, будь ласка, іншу статтю🤗")
        start_news(call.message)


bot.polling(none_stop=True)
