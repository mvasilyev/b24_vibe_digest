import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from database.engine import init_db
from handlers import common, message
from services.scraper import ScraperService
from services.llm_service import LLMService

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

async def main():
    # Инициализация БД
    logger.info("Initializing database...")
    await init_db()

    # Инициализация сервисов
    scraper = ScraperService()
    llm = LLMService()

    # Инициализация бота
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    # Регистрация роутеров
    dp.include_router(common.router)
    
    # В aiogram 3.x мы можем передавать объекты через dp.middleware или аргументы
    # Для простоты в MVP, прокидываем через context (в данном случае через dp аргументы)
    dp["scraper"] = scraper
    dp["llm"] = llm

    dp.include_router(message.router)

    logger.info("Bot is starting polling...")
    try:
        await dp.start_polling(bot)
    finally:
        await scraper.close()
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
