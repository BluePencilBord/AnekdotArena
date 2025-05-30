from unittest.mock import AsyncMock, MagicMock
import pytest
from bot.anecdotes.router import start_write_anecdote, process_anecdote, rate_anecdote, process_rate
from pydantic import ValidationError

@pytest.mark.asyncio
async def test_start_write_anecdote(fake_callback, fake_state):
    await start_write_anecdote(fake_callback, fake_state)

    fake_callback.message.edit_text.assert_called_once()
    fake_state.set_state.assert_called_once()

@pytest.mark.asyncio
async def test_process_anecdote_success(
    fake_message, fake_state, fake_session
):
    from bot.users.dao import UserDAO
    from bot.anecdotes.dao import AnecdoteDAO
    from bot.users.utils import get_start_text

    UserDAO.find_one_or_none = AsyncMock(return_value=MagicMock(id=123))
    AnecdoteDAO.add = AsyncMock()
    get_start_text = AsyncMock(return_value=("Текст", None))

    await process_anecdote(
        fake_message, fake_state, fake_session, fake_session
    )

    fake_message.answer.assert_called_with("✅ Ваш анекдот успешно сохранен!")

@pytest.mark.asyncio
async def test_rate_anecdote(fake_callback, fake_state, fake_session):
    from bot.users.dao import UserDAO
    from bot.anecdotes.dao import RateDAO
    from bot.anecdotes.utils import send_next_anecdote

    UserDAO.find_one_or_none = AsyncMock(return_value=MagicMock(id=123))
    RateDAO.find_all = AsyncMock(return_value=[])
    send_next_anecdote = AsyncMock()

    await rate_anecdote(fake_callback, fake_state, fake_session)

    fake_callback.answer.assert_called_once()
    send_next_anecdote.assert_awaited_once()

@pytest.mark.asyncio
async def test_process_rate(fake_callback, fake_state, fake_session):
    from bot.anecdotes.dao import RateDAO
    from bot.anecdotes.utils import send_next_anecdote

    RateDAO.add = AsyncMock()
    send_next_anecdote = AsyncMock()

    fake_callback_data = MagicMock()
    fake_callback_data.value = 5

    await process_rate(
        fake_callback, fake_callback_data, fake_state,
        fake_session, fake_session
    )

    RateDAO.add.assert_awaited_once()
    fake_callback.message.edit_reply_markup.assert_called_once()
    send_next_anecdote.assert_awaited_once()