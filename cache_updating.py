from parse import *
from gpt import *
import json


def split_message(msg: str) -> list[str]:
    """Split the text into parts considering Telegram limits."""
    parts = []
    while msg:
        max_msg_length = 4000
        if len(msg) <= max_msg_length:
            parts.append(msg)
            break
        part = msg[:max_msg_length]
        first_ln = part.rfind("\n")
        if first_ln != -1:
            new_part = part[:first_ln]
            parts.append(new_part)
            msg = msg[first_ln + 1:]
            continue
        first_space = part.rfind(" ")
        if first_space != -1:
            new_part = part[:first_space]
            parts.append(new_part)
            msg = msg[first_space + 1:]
            continue
        parts.append(part)
        msg = msg[max_msg_length:]
    return parts


def update_cache():
    with open("cache.json", encoding="utf-8") as file:
        database = json.load(file)

    editions = {"BBC": [parse_list_bbc, parse_text_bbc],
                "CNN": [parse_list_cnn, parse_text_cnn],
                "Bild": [parse_list_bild, parse_text_bild],
                "Spiegel": [parse_list_spiegel, parse_text_spiegel]}

    for edition in editions.keys():
        list_of_news = editions[edition][0]()
        get_text_function = editions[edition][1]
        for key, value in list_of_news.items():
            try:
                if edition not in database:
                    database[edition] = {}
                items = list(database[edition].items())
                if key not in database[edition]:
                    if len(database[edition]) == 5:
                        items.pop()
                    database[edition].clear()
                    label = value
                    label_translation = get_gpt_answer(label, label_translate)

                    text_news = split_message(get_text_function("", key))
                    translation_text = split_message(get_gpt_answer(str(text_news), sample_translate))

                    retelling = split_message(get_gpt_answer(str(text_news), sample_retell))

                    database[edition] = {key: [
                        {"label": label},
                        {"label_translation": label_translation},
                        {"text": text_news},
                        {"text_translation": translation_text},
                        {"retelling": retelling}
                    ]}
                    database[edition].update(items)
            except Exception as e:
                continue

    with open('cache.json', 'w', encoding="utf-8") as file:
        json.dump(database, file, indent=4, ensure_ascii=False)

