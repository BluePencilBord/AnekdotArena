from unittest.mock import AsyncMock, MagicMock
import pytest
from bot.anecdotes.router import (
    start_write_anecdote,
    process_anecdote,
    rate_anecdote,
    process_rate,
)
from unittest.mock import patch


@pytest.mark.asyncio
async def test_start_write_anecdote(fake_callback, fake_state):
    await start_write_anecdote(fake_callback, fake_state)

    fake_callback.message.edit_text.assert_called_once()
    fake_state.set_state.assert_called_once()


@pytest.mark.asyncio
async def test_process_anecdote_success(fake_message, fake_state, fake_session):
    from bot.users.dao import UserDAO
    from bot.anecdotes.dao import AnecdoteDAO

    UserDAO.find_one_or_none = AsyncMock(return_value=MagicMock(id=123))
    AnecdoteDAO.add = AsyncMock()

    with patch(
        "bot.anecdotes.router.get_start_text",
        new=AsyncMock(return_value=("Текст", None)),
    ):
        await process_anecdote(fake_message, fake_state, fake_session, fake_session)

    fake_message.answer.assert_any_call("✅ Ваш анекдот успешно сохранен!")


@pytest.mark.asyncio
async def test_rate_anecdote(fake_callback, fake_state, fake_session):
    from bot.users.dao import UserDAO
    from bot.anecdotes.dao import RateDAO, AnecdoteDAO

    UserDAO.find_one_or_none = AsyncMock(return_value=MagicMock(id=123))
    RateDAO.find_all = AsyncMock(return_value=[])

    AnecdoteDAO.find_one_random_not_in = AsyncMock(
        return_value=MagicMock(
            id=1, content="Тестовый анекдот", user_id=123, report_count=0
        )
    )

    await rate_anecdote(fake_callback, fake_state, fake_session)


@pytest.mark.asyncio
async def test_process_rate(fake_callback, fake_state, fake_session):
    from bot.anecdotes.dao import RateDAO, AnecdoteDAO

    RateDAO.add = AsyncMock()

    with patch(
        "bot.anecdotes.router.send_next_anecdote", new_callable=AsyncMock
    ) as mock_send_next_anecdote:
        AnecdoteDAO.find_one_random_not_in = AsyncMock(
            return_value=MagicMock(
                id=1, content="Тестовый анекдот", user_id=123, report_count=0
            )
        )

        fake_callback_data = MagicMock()
        fake_callback_data.value = 5

        await process_rate(
            fake_callback, fake_callback_data, fake_state, fake_session, fake_session
        )

        RateDAO.add.assert_awaited()
        mock_send_next_anecdote.assert_awaited()
