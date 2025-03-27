import asyncio
import json
from utils.parse import *
from utils.gpt import *


def split_message(msg: str) -> list[str]:
    """Split the text into parts considering Telegram limits (4000 characters) without breaking sentences."""
    parts = []
    max_msg_length = 4000

    while msg:
        if len(msg) <= max_msg_length:
            parts.append(msg)
            break

        part = msg[:max_msg_length]
        last_dot = part.rfind(". ")
        if last_dot != -1:
            new_part = part[:last_dot + 1]
            parts.append(new_part.strip())
            msg = msg[last_dot + 2:].strip()
            continue

        last_dot = part.rfind(".")
        if last_dot != -1:
            new_part = part[:last_dot + 1]
            parts.append(new_part.strip())
            msg = msg[last_dot + 1:].strip()
            continue

        last_ln = part.rfind("\n")
        if last_ln != -1:
            new_part = part[:last_ln]
            parts.append(new_part.strip())
            msg = msg[last_ln + 1:].strip()
            continue

        last_space = part.rfind(" ")
        if last_space != -1:
            new_part = part[:last_space]
            parts.append(new_part.strip())
            msg = msg[last_space + 1:].strip()
            continue

        parts.append(part.strip())
        msg = msg[max_msg_length:].strip()

    return parts


def update_cache():
    with open("utils/cache.json", encoding="utf-8") as file:
        database = json.load(file)

    editions = {"BBC": [parse_list_bbc, parse_text_bbc],
                "CNN": [parse_list_cnn, parse_text_cnn],
                "Bild": [parse_list_bild, parse_text_bild],
                "Spiegel": [parse_list_spiegel, parse_text_spiegel]}

    for edition in editions.keys():
        list_of_news = editions[edition][0]()
        get_text_function = editions[edition][1]
        for url, label in list_of_news.items():
            try:
                if edition not in database:
                    database[edition] = {}
                items = list(database[edition].items())
                if url not in database[edition]:
                    if len(database[edition]) == 5:
                        items.pop()
                    database[edition].clear()

                    raw_text = get_text_function(url)
                    formatted_text = f"<b>{label}</b>\n\n"
                    text_news = split_message(formatted_text + raw_text)

                    label_translation = get_gpt_answer(label, label_translate)

                    formatted_translation = f"<b>{label_translation}</b>\n\n"
                    translation_text = split_message(
                        formatted_translation + get_gpt_answer(raw_text, sample_translate)
                    )

                    formatted_retelling = f"<b>{label_translation}</b>\n\n"
                    retelling = split_message(
                        formatted_retelling + get_gpt_answer(raw_text, sample_retell)
                    )

                    database[edition] = {url: [
                        {"label": label},
                        {"label.translation": label_translation},
                        {"text": text_news},
                        {"text.translation": translation_text},
                        {"retelling": retelling}
                    ]}
                    database[edition].update(items)
            except Exception as e:
                continue

    with open('utils/cache.json', 'w', encoding="utf-8") as file:
        json.dump(database, file, indent=4, ensure_ascii=False)


async def run_update_cache():
    while True:
        update_cache()
        await asyncio.sleep(3600)