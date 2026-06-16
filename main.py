import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database.engine import init_db
from handlers import common, message
from services.scraper import ScraperService
from services.llm_service import LLMService
from services.digest import DigestService

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

    # Инициализация бота
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    # Инициализация сервисов
    scraper = ScraperService()
    llm = LLMService()
    digest_service = DigestService(bot)

    # Регистрация роутеров
    dp.include_router(common.router)
    
    # Прокидываем сервисы в dp для доступа в хендлерах
    dp["digest_service"] = digest_service
    dp["scraper"] = scraper
    dp["llm"] = llm
    
    dp.include_router(message.router)

    # Настройка планировщика
    scheduler = AsyncIOScheduler()
    
    # Получаем время из конфига (формат HH:MM)
    digest_time_str = os.getenv("DIGEST_TIME", "09:00")
    try:
        hour, minute = map(int, digest_time_str.split(":"))
        
        # Устанавливаем расписание через CRON
        scheduler.add_job(
            digest_service.send_daily_digest_to_all, 
            "cron", 
            hour=hour, 
            minute=minute
        )
        logger.info(f"Scheduled daily digest at {hour:02d}:{minute:02d}")
    except ValueError:
        logger.error(f"Invalid DIGEST_TIME format: {digest_time_str}. Expected HH:MM. Scheduler not started.")
        # Если формат неверный, можно либо упасть, либо оставить интервал. 
        # Для надежности в продакшене лучше упасть, чтобы админ узнал.

    scheduler.start()

    logger.info("Bot is starting polling...")
    try:
        await dp.start_polling(bot)
    finally:
        scheduler.shutdown()
        await scraper.close()
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
