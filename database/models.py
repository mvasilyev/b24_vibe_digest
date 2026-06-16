from sqlalchemy import String, Text, DateTime, Boolean, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from .engine import Base

class ContentItem(Base):
    __tablename__ = "content_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)
    
    # Тип контента: 'text' (сообщение) или 'url' (ссылка)
    content_type: Mapped[str] = mapped_column(String(20), default="text")
    
    # Оригинальное содержимое (текст сообщения или сам URL)
    original_content: Mapped[str] = mapped_column(Text)
    
    # Извлеченный текст из ссылки (если это URL)
    extracted_text: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Результат работы LLM
    summary: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Метаданные
    title: Mapped[str] = mapped_column(String(500), nullable=True)
    image_url: Mapped[str] = mapped_column(String(1000), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    is_processed: Mapped[bool] = mapped_column(Boolean, default=False)
    is_sent_in_digest: Mapped[bool] = mapped_column(Boolean, default=False)
