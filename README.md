
---

# News Sender Telegram Bot

This project is a Telegram bot that automatically collects information from several online news editions, translates the content, summarizes it, and caches the results in a structured format. The bot is built using `aiogram`, `requests`, `beautifulsoup4`, and `g4f`.

## Features

- Parses news from multiple online editions
- Automatically translates:
  - Article titles
  - Full text
  - Summarized (retold) content
- Saves structured data to a cache file
- Interacts with users through a Telegram bot
- Stores and logs user feedback

## Example Cache Format (`cache.json`)

```json
{
  "edition": {
    "https://edition": [
      { "label": "label of news" },
      { "label.translation": "Переклад назви" },
      { "text": ["Text part1", "Text part2"] },
      { "text.translation": ["Переклад частина 1", "Переклад частина 2"] },
      { "retelling": ["Переказ частина 1", "Переказ частина 2"] }
    ]
  }
}
```

## Technologies Used

- `aiogram` – for Telegram bot interactions
- `requests` – for HTTP requests
- `beautifulsoup4` (`bs4`) – for parsing HTML content
- `g4f` – for translation and retelling using generative AI
- `dotenv` – for managing environment variables

## Project Structure

```
news_sender/
├── app/
│   ├── handlers.py       # Telegram bot message handlers
│   └── keyboards.py      # Reply keyboards (if any)
├── utils/
│   ├── cache_updating.py # Periodic cache updater
│   ├── gpt.py            # GPT-related logic (translation/retelling)
│   ├── parse.py          # HTML parsing of editions
│   └── translate.py      # Translation functions
├── feedback.json         # User feedback stored here
├── cache.json            # Cached translated and summarized news
├── main.py               # Entry point to run the bot
├── .env                  # Contains the Telegram Bot token
└── .gitignore
```

## How to Run

1. Create a `.env` file with your Telegram bot token:
   ```
   TOKEN=your_telegram_bot_token_here
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the bot:
   ```bash
   python main.py
   ```

---