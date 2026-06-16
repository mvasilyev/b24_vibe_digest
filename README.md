# 📝 TG Digest Bot

Personal Telegram bot for content curation. Send links or forward messages, and get a clean, AI-powered daily digest.

## ✨ Features

- 🔗 **Smart Link Scraping**: Automatically extracts titles and content from articles and websites, stripping away ads and junk.
- 🧠 **AI-Powered Summaries**: Uses LLM to transform long articles or forwarded messages into concise, readable summaries.
- 📅 **Scheduled Digests**: Get your curated content delivered at a specific time every day.
- ⚡ **Instant Digest**: Use the `/digest` command to get your accumulated summary immediately.
- 🛠 **Fully Configurable**: Control everything (model, API, schedule) via a simple `.env` file.

## 🛠 Tech Stack

- **Language**: Python 3.10+
- **Bot Framework**: [aiogram 3.x](https://docs.aiogram.dev/) (Asynchronous)
- **Database**: [SQLite](https://www.sqlite.org/) with [SQLAlchemy 2.0](https://docs.sqlalchemy.org/) (Async)
- **Task Scheduling**: [APScheduler](https://apscheduler.readthedocs.io/)
- **Scraping**: [trafilatura](https://trafilatura.readthedocs.io/) & [httpx](https://www.python-httpx.org/)
- **LLM Integration**: OpenAI-compatible API (works with OpenAI, DeepSeek, Ollama, etc.)

## 🚀 Setup & Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd tg_digest_bot
```

### 2. Create and activate a virtual environment
**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configuration
Create a `.env` file in the `tg_digest_bot/` directory based on the template:
```bash
cp .env.example .env
```

Edit the `.env` file with your credentials:
- `BOT_TOKEN`: Your Telegram Bot Token from [@BotFather](https://t.me/botfather).
- `LLM_API_KEY`: Your API key for the LLM provider.
- `LLM_BASE_URL`: The API endpoint (e.g., `https://api.openai.com/v1` or `http://localhost:11434/v1` for Ollama).
- `LLM_MODEL_NAME`: The model you want to use (e.g., `gpt-4o-mini`, `deepseek-chat`, `llama3`).
- `DIGEST_TIME`: The time for the daily digest in `HH:MM` format (e.g., `09:00`).

## 🕹 Usage

1. **Start the bot**:
   ```bash
   python main.py
   ```
2. **Add content**: 
   - Send a URL (e.g., `https://example.com/article`).
   - Forward a message from any Telegram channel.
3. **Get your digest**:
   - Wait for the scheduled time.
   - Or type `/digest` to get it immediately.

## 📝 License

MIT
