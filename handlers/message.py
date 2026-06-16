import re
import asyncio
import logging
from aiogram import Router, types
from sqlalchemy import select

from database.engine import AsyncSessionLocal
from database.models import ContentItem
from services.scraper import ScraperService
from services.llm_service import LLMService

logger = logging.getLogger(__name__)
router = Router()

# Регулярка для поиска URL
URL_PATTERN = re.compile(r'https?://\S+')

async def process_content_task(user_id: int, item_id: int, url: str, scraper: ScraperService, llm: LLMService):
    """
    Фоновая задача для обработки ссылки: скрапинг -> саммари -> обновление БД.
    """
    logger.info(f"Starting background processing for item {item_id} (user {user_id})")
    
    # 1. Скрапинг
    scraped_data = await scraper.scrape_url(url)
    
    async with AsyncSessionLocal() as session:
        async with session.begin():
            # Ищем наш объект
            stmt = select(ContentItem).where(ContentItem.id == item_id)
            result = await session.execute(stmt)
            item = result.scalar_one_or_none()
            
            if not item:
                logger.error(f"Item {item_id} not found in DB during background task")
                return

            if scraped_data:
                item.extracted_text = scraped_data.get("text")
                item.title = scraped_data.get("title")
                
                # 2. LLM Summary
                if item.extracted_text:
                    summary = await llm.summarize(item.extracted_text)
                    item.summary = summary
            
            item.is_processed = True
        
        await session.commit()
    
    logger.info(f"Finished background processing for item {item_id}")

@router.message()
async def handle_message(message: types.Message, scraper: ScraperService, llm: LLMService):
    """
    Основной обработчик входящих сообщений.
    """
    user_id = message.from_user.id
    text = message.text or message.caption or ""
    
    if not text:
        return

    # Ищем URL в тексте
    urls = URL_PATTERN.findall(text)
    
    async with AsyncSessionLocal() as session:
        async with session.begin():
            if urls:
                # Если нашли URL, создаем запись типа 'url'
                # Берем первый найденный URL для простоты
                url = urls[0]
                new_item = ContentItem(
                    user_id=user_id,
                    content_type="url",
                    original_content=url
                )
                session.add(new_item)
                await session.flush() # Чтобы получить item.id
                item_id = new_item.id
                
                await message.answer("🔗 Ссылка получена! Я изучу её и добавлю в дайджест.")
                
                # Запускаем фоновую обработку
                asyncio.create_task(process_content_task(user_id, item_id, url, scraper, llm))
            else:
                # Если это просто текст (или форвард сообщения без ссылок)
                new_item = ContentItem(
                    user_id=user_id,
                    content_type="text",
                    original_content=text
                )
                session.add(new_item)
                await message.answer("📝 Текст сохранен. Добавлю в дайджест.")
