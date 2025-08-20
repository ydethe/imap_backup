from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file_encoding="utf-8",
        extra="allow",
    )

    LOGLEVEL: str = "info"
    MAILDIR_FOLDER: Path = Path(".")
    SERVER: str = "localhost"
    PORT: int = 993
    USERNAME: str = "foo"
    PASSWORD: str = "bar"
    MAILBOX: str = "INBOX"
