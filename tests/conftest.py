import pytest
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def fake_callback():
    callback = AsyncMock()
    callback.from_user.id = 123
    callback.data = "some_data"
    callback.message = AsyncMock()
    return callback

@pytest.fixture
def fake_message():
    msg = AsyncMock()
    msg.from_user.id = 123
    msg.text = "Смешной анекдот"
    return msg

@pytest.fixture
def fake_state():
    state = AsyncMock()
    state.get_data = AsyncMock(return_value={
        "anecdote_id": 1,
        "user_id": 123,
        "rated_anecdote_ids": [],
        "anecdote_report_count": 0
    })
    return state

@pytest.fixture
def fake_session():
    return AsyncMock()
