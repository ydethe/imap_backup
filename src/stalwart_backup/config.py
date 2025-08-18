from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class ImapConfiguration(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        extra="allow",
    )

    LABEL: str
    IMAP_SERVER: str
    IMAP_PORT: int
    USERNAME: str
    PASSWORD: str
    MAILBOX: str


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
        env_nested_delimiter="__",
    )

    LOGLEVEL: str
    MBOX_FILE: Path
    IMAP: ImapConfiguration
    SYNC_PERIOD: int


config = Config()
