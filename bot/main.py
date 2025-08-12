import asyncio
import logging
from aiogram.types import BotCommand, BotCommandScopeDefault
from bot.config_reader import bot, dp
from bot.users.router import user_router
from bot.anecdotes.router import anecdote_router
from bot.payments.router import payments_router
from bot.admins.router import admin_router
from bot.metrics import start_metrics_server
from bot.database.models import *  # noqa
from bot.database.dao.databae_middleware import (
    DatabaseMiddlewareWithoutCommit,
    DatabaseMiddlewareWithCommit,
)

logging.basicConfig(level=logging.INFO)


async def set_commands():
    commands = [
        BotCommand(command="start", description="Старт"),
        BotCommand(command="contact_us", description="Обратная связь"),
        BotCommand(command="paysupport", description="Помощь по вопросам оплаты"),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def main():
    dp.update.middleware.register(DatabaseMiddlewareWithoutCommit())
    dp.update.middleware.register(DatabaseMiddlewareWithCommit())

    dp.include_router(user_router)
    dp.include_router(anecdote_router)
    dp.include_router(payments_router)
    dp.include_router(admin_router)

    start_metrics_server(port=8000)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
