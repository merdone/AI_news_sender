from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import asyncio
import json

from app.keyboards import *

router = Router()

user_message_history = {}
history_lock = asyncio.Lock()

convert_action_to_index = {"label": 0,
                           "label.translation": 1,
                           "text": 2,
                           "text.translation": 3,
                           "retelling": 4}
FEEDBACK_FILE = "feedback.json"


class Feedback(StatesGroup):
    feedback = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer_sticker("CAACAgIAAxkBAAECo79ljVIJMGtC055ZKwT24S50L81lHAAC2A8AAkjyYEsV-8TaeHRrmDME")
    await message.answer("Для того, щоб почати роботу, оберіть статтю, натиснувши на кнопку знизу 👇",
                         reply_markup=first_message)


@router.message(F.text == '📜 Список джерел')
async def get_list_of_editions(message: Message):
    await message.answer("<b>Оберіть джерело, з якого брати статтю:</b>",
                         reply_markup=await edition_choice(), parse_mode="html")


def save_feedback(user_id, feedback):
    with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    user_id_str = str(user_id)
    if user_id_str not in data:
        data[user_id_str] = []
    data[user_id_str].append(feedback)
    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@router.message(F.text == "✉ Залишити відгук")
async def get_feedback(message: Message, state: FSMContext):
    await state.set_state(Feedback.feedback)
    await message.answer("Введіть Ваш відгук: ")


@router.message(Feedback.feedback)
async def collecting_feedback(message: Message, state: FSMContext):
    await state.update_data(feedback=message.text)
    data = await state.get_data()
    feedback = data["feedback"]
    save_feedback(message.from_user.id, feedback)
    await message.answer("Дякую за твій відгук!")
    await state.clear()


async def delete_old_messages(callback: CallbackQuery):
    user_id = callback.from_user.id
    async with history_lock:
        if user_id in user_message_history:
            for msg_id in user_message_history[user_id]:
                try:
                    await callback.bot.delete_message(callback.message.chat.id, msg_id)
                except:
                    pass
            user_message_history[user_id].clear()


async def cleanup_old_entries(interval_seconds=3600):
    while True:
        await asyncio.sleep(interval_seconds)
        async with history_lock:
            user_message_history.clear()


@router.callback_query(F.data.startswith("edition_"))
async def edition_callback_handler(callback: CallbackQuery):
    await delete_old_messages(callback)
    message = ""
    title_number = 1
    edition_name = callback.data.split("_")[1]
    with open("cache.json", encoding="utf-8") as file:
        database = json.load(file)
    temp_database = database[edition_name]
    for key in temp_database.keys():
        message += f"{title_number} - {temp_database[key][1]["label.translation"]}\n\n"
        title_number += 1
    await callback.message.edit_text(message,
                                     reply_markup=await news_choice(temp_database.keys(), edition_name, "text"))
    await callback.answer()


@router.callback_query(F.data == "change_edition")
async def end_work_handler(callback: CallbackQuery):
    await callback.message.delete()
    await delete_old_messages(callback)
    await get_list_of_editions(callback.message)


@router.callback_query(F.data.startswith("get_from_cache"))
async def getting_info_callback_handler(callback: CallbackQuery):
    type_of_work = callback.data.split("_")[3]
    edition_name = callback.data.split("_")[4]
    index = int(callback.data.split("_")[5])

    with open("cache.json", encoding="utf-8") as file:
        database = json.load(file)

    temp_database = database[edition_name]
    link = list(temp_database.keys())[index]
    index_of_action = convert_action_to_index[type_of_work]
    message = temp_database[link][index_of_action][type_of_work]
    last_message_text = callback.message.text

    if last_message_text[:100] == message[-1][:100]:
        await callback.answer("Цю дію вже зроблено")
        return

    await delete_old_messages(callback)

    if len(message) == 1:
        try:
            await callback.message.edit_text(message[0], reply_markup=await action_choice(edition_name, index),
                                             parse_mode="html")
        except Exception as e:
            await callback.answer("Цю дію вже зроблено")
    else:
        await callback.message.delete()
        previous_msgs = []
        for i in range(len(message) - 1):
            msg = await callback.message.answer(message[i], parse_mode="html")
            previous_msgs.append(msg.message_id)
        await callback.message.answer(message[-1], reply_markup=await action_choice(edition_name, index),
                                      parse_mode="html")
        user_message_history[callback.from_user.id] = previous_msgs
    await callback.answer()
