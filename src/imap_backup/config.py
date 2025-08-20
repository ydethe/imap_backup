from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file_encoding="utf-8",
    )

    loglevel: str = "info"
    maildir_folder: Path = Path(".")
    server: str = "localhost"
    port: int = 993
    username: str = "foo"
    password: str = "bar"
    mailbox: str = "INBOX"
