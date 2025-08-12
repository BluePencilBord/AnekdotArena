from bot.users.dao import UserDAO
from bot.users.kbs import main_user_kb
from bot.users.schemas import TelegramIDModel, UserModel
from bot.anecdotes.dao import RateDAO
from bot.anecdotes.schemas import RateModelUserId
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from bot.payments.dao import DonationDAO


async def get_start_text(message: Message, session: AsyncSession) -> tuple[str, dict]:
    user_info = await UserDAO.find_one_or_none(
        session=session, filters=TelegramIDModel(telegram_id=message.from_user.id)
    )

    total_donation = await DonationDAO.sum_amount(session)

    if not user_info:
        values = UserModel(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
        )

        user_info = await UserDAO.add(session=session, values=values)

    rates = await RateDAO.count(session, filters=RateModelUserId(user_id=user_info.id))

    text = f"⚔️ Добро пожаловать на <b>Анекдот Арену</b> 🛡️\n\n🎁 Пиши шутки и зарабатывай ⭐\n\n💰 Призовой фонд: <b>{total_donation}</b> ⭐️\n\n📝 Оценил анекдотов: <b>{rates}</b> 🔎"
    kb = main_user_kb(message.from_user.id)

    return text, kb
