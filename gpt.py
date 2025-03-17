from g4f.client import Client

sample_retell = "Переказуй текст українською мовою, точно передаючи всі назви, дотримуйтесь 500 слів, не вітайтеся на " \
                "початок повідомлення і не додавайте свої коментарі. Відразу починайте розповідь без вступний слів. " \
                "Не рахуй кількість слів у кінці та напочатку. Не пиши нічого переред переказом і після. ТІЛЬКИ " \
                "ПЕРЕКАЗ І НІЧОГО БІЛЬШЕ. "

sample_translate = "Translate to the Ukrainian all of the text as accurately as possible, without unnecessary words, " \
                   "leaving all names and without adding unnecessary words. Don't repeat the request and don't say " \
                   "hello first. "

client = Client()


def get_gpt_answer(text, sample):
    result = ""
    content = sample + text
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": content}],
        web_search=False,
    )
    return response.choices[0].message.content
