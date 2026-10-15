from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# backend/.env, resolved from this file so it is found no matter
# which directory a command is started from.
ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    """Application settings, read from environment variables and backend/.env.

    Environment variables take precedence over values in the .env file.
    Names are case-insensitive: DATABASE_URL sets `database_url`.
    """

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")

    app_name: str = "Shop API"
    database_url: str
    # Only used by the test suite (see tests/conftest.py).
    test_database_url: str | None = None
    # Log every SQL statement. Handy for debugging, noisy otherwise.
    sql_echo: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
