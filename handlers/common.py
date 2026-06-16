from aiogram import Router, types
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я твой персональный бот-дайджест. 📝\n\n"
        "Просто присылай мне ссылки на интересные статьи или форварди сообщения из каналов. "
        "Раз в день я буду собирать всё это в удобный дайджест с краткими описаниями.\n\n"
        "Пока что я только учусь, но скоро буду готов!"
    )
