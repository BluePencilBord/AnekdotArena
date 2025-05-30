from unittest.mock import AsyncMock
import pytest
import os
from dotenv import load_dotenv

env_content = """\
BOT_TOKEN=1234567890:qwertyuiopasdfghjklzxcvbnmqwertyuio
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=testDB
POSTGRES_PORT=1234
POSTGRES_HOST=host
ADMIN_IDS=[123456789]
REDIS_HOST=user
REDIS_PORT=1234
"""

temp_env_path = os.path.join(os.path.dirname(__file__), ".env.test")
with open(temp_env_path, "w") as f:
    f.write(env_content)

load_dotenv(dotenv_path=temp_env_path, override=True)


@pytest.fixture(scope="session", autouse=True)
def cleanup_env():
    yield
    if os.path.exists(temp_env_path):
        os.remove(temp_env_path)


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
    state.get_data = AsyncMock(
        return_value={
            "anecdote_id": 1,
            "user_id": 123,
            "rated_anecdote_ids": [],
            "anecdote_report_count": 0,
        }
    )
    return state


@pytest.fixture
def fake_session():
    return AsyncMock()
