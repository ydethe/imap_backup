from pathlib import Path
from typing_extensions import Annotated

import typer

from .config import Config
from .imap_sync import sync_all


app = typer.Typer()


@app.command()
def imap_backup(
    host: Annotated[str, typer.Argument(help="IMAP server address", envvar="SERVER")],
    username: Annotated[str, typer.Argument(envvar="USERNAME")],
    password: Annotated[str, typer.Option(prompt=True, hide_input=True)],
    output: Annotated[Path, typer.Option(envvar="MAILDIR_FOLDER")] = Path("."),
    port: Annotated[int, typer.Option(envvar="PORT")] = 993,
    mailbox: Annotated[str, typer.Option(envvar="MAILBOX")] = "INBOX",
    loglevel: Annotated[str, typer.Option(envvar="LOGLEVEL")] = "INFO",
):
    config = Config(
        loglevel=loglevel,
        maildir_folder=output,
        server=host,
        port=port,
        username=username,
        password=password,
        mailbox=mailbox,
    )

    sync_all(config)
