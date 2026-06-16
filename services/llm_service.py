from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=os.getenv("LLM_API_KEY"),
            base_url=os.getenv("LLM_BASE_URL")
        )
        self.model_name = os.getenv("LLM_MODEL_NAME", "gpt-4o-mini")

    async def summarize(self, text: str) -> str:
        """
        Делает краткое саммари текста.
        """
        if not text or len(text) < 50:
            return text

        truncated_text = text[:10000]

        prompt = (
            "Ты — помощник, который делает краткие и емкие саммари для дайджеста. "
            "Прочитай текст ниже и напиши содержательное резюме на русском языке. "
            "Выдели самую суть. Не используй вводные фразы типа 'В данном тексте говорится...'. "
            "Пиши сразу по делу.\n\n"
            f"ТЕКСТ:\n{truncated_text}"
        )

        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes text in Russian."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                # Модель reasoning-типа тратит часть бюджета на reasoning_content,
                # поэтому лимит должен покрывать и рассуждения, и сам ответ.
                max_tokens=4000
            )
            choice = response.choices[0]
            content = choice.message.content
            if not content:
                logger.error(
                    f"LLM returned empty content (finish_reason={choice.finish_reason})"
                )
                return "Не удалось создать саммари."
            return content.strip()
        except Exception as e:
            logger.exception(f"LLM Error: {e}")
            return "Не удалось создать саммари."
