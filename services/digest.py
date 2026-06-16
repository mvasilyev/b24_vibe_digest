import logging
from sqlalchemy import select
from database.engine import AsyncSessionLocal
from database.models import ContentItem
from aiogram import Bot

logger = logging.getLogger(__name__)

class DigestService:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def send_user_digest(self, user_id: int) -> bool:
        """
        Собирает и отправляет дайджест конкретному пользователю.
        Возвращает True, если были отправлены новые записи, иначе False.
        """
        async with AsyncSessionLocal() as session:
            # 1. Получаем все новые записи для пользователя
            stmt_items = select(ContentItem).where(
                ContentItem.user_id == user_id,
                ContentItem.is_sent_in_digest == False
            ).order_by(ContentItem.created_at.desc())
            
            result_items = await session.execute(stmt_items)
            items = result_items.scalars().all()

            if not items:
                return False

            # 2. Формируем сообщение
            digest_text = "🌟 **Твой дайджест** 🌟\n\n"
            
            for item in items:
                if item.content_type == "url":
                    title = item.title if item.title else "Без заголовка"
                    summary = item.summary if item.summary else "Описание недоступно."
                    digest_text += f"🔗 [{title}]({item.original_content})\n"
                    digest_text += f"_{summary}_\n\n"
                else:
                    # Обычный текст
                    digest_text += f"📝 *Сообщение:*\n_{item.original_content}_\n\n"
                
                # Помечаем как отправленное
                item.is_sent_in_digest = True

            # Обрезаем, если дайджест слишком длинный (лимит TG ~4096)
            if len(digest_text) > 4000:
                digest_text = digest_text[:3900] + "\n\n... (дайджест слишком длинный, сокращен)"

            # 3. Отправляем
            try:
                await self.bot.send_message(user_id, digest_text, parse_mode="Markdown")
                await session.commit()
                logger.info(f"Digest sent to user {user_id}")
                return True
            except Exception as e:
                logger.error(f"Failed to send digest to {user_id}: {e}")
                return False

    async def send_daily_digest_to_all(self):
        """
        Рассылка всем пользователям (для планировщика).
        """
        async with AsyncSessionLocal() as session:
            # Находим всех пользователей, у которых есть новые записи
            stmt_users = select(ContentItem.user_id).where(ContentItem.is_sent_in_digest == False).distinct()
            result_users = await session.execute(stmt_users)
            user_ids = result_users.scalars().all()

            if not user_ids:
                logger.info("No new content to digest for anyone.")
                return

            for user_id in user_ids:
                await self.send_user_digest(user_id)
