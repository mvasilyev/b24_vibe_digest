from aiogram import Router, types
from aiogram.filters import CommandStart, Command

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я твой персональный бот-дайджест. 📝\n\n"
        "Просто присылай мне ссылки на интересные статьи или форварди сообщения из каналов. "
        "Раз в день я буду собирать всё это в удобный дайджест с краткими описаниями.\n\n"
        "Пока что я только учусь, но скоро буду готов!"
    )

@router.message(Command("digest"))
async def cmd_digest(message: types.Message, digest_service):
    """
    Команда для нетерпеливых: получить дайджест прямо сейчас.
    """
    from services.digest import DigestService
    sent = await digest_service.send_user_digest(message.from_user.id)
    if sent:
        await message.answer("✅ Твой дайджест готов и отправлен выше!")
    else:
        await message.answer("📭 У тебя пока нет новых сообщений для дайджеста.")
