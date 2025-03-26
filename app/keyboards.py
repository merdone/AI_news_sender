from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

editions = ["BBC", "CNN", "Bild", "Spiegel"]

actions = {"text.translation": "Перекласти", "retelling": "Переказати", "text": "Показати оригінал",
           "change_another_news": "Обрати іншу статтю", "change_edition": "Обрати інше джерело"}

first_message = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="📜 Список джерел"), KeyboardButton(text="✉ Залишити відгук")]], resize_keyboard=True)


async def edition_choice():
    keyboard = InlineKeyboardBuilder()
    for edition in editions:
        keyboard.add(InlineKeyboardButton(text=edition, callback_data=f"edition_{edition}"))
    return keyboard.adjust(1).as_markup()


async def news_choice(data, edition_name, type_of_work):
    title_number = 1
    keyboard = InlineKeyboardBuilder()
    for key in data:
        keyboard.add(InlineKeyboardButton(text=f"{title_number}",
                                          callback_data=f"get_from_cache_{type_of_work}_{edition_name}_{title_number - 1}"))
        title_number += 1
    keyboard.add(InlineKeyboardButton(text=actions["change_edition"], callback_data="change_edition"))
    return keyboard.adjust(1).as_markup()


async def action_choice(edition_name, index):
    keyboard = InlineKeyboardBuilder()
    for action in actions.keys():
        if action == "change_edition":
            keyboard.add(InlineKeyboardButton(text=actions[action], callback_data=action))
        elif action == "change_another_news":
            keyboard.add(InlineKeyboardButton(text=actions[action], callback_data=f"edition_{edition_name}"))
        else:
            keyboard.add(InlineKeyboardButton(text=actions[action],
                                              callback_data=f"get_from_cache_{action}_{edition_name}_{index}"))
    return keyboard.adjust(1).as_markup()
