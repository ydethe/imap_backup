import imaplib
from pathlib import Path
from typing import List

from .config import config, ImapConfiguration
from . import logger


def connect_to_imap(cfg: ImapConfiguration) -> imaplib.IMAP4_SSL:
    """Connect to the IMAP server

    Args:
        cfg: Connection information

    Returns:
        A object to interact with the IMAP server

    """
    mail = imaplib.IMAP4_SSL(cfg.IMAP_SERVER, cfg.IMAP_PORT)
    mail.login(cfg.USERNAME, cfg.PASSWORD)
    return mail


def sync_mailbox(mail: imaplib.IMAP4_SSL, label: str, mailbox: str):
    """
    Download and process emails

    Args:
        mail: Handler to the IMAP server, got with a call to `connect_to_imap`
        mailbox: Name of the mailbox to download emails from

    """
    try:
        typ, data = mail.select(mailbox, readonly=True)
    except Exception:
        typ = "NO"
    if typ != "OK":
        logger.warning(f"Failed to select mailbox: {mailbox}")
        return

    filter = "ALL"
    typ, data = mail.uid("search", None, filter)
    if typ != "OK":
        logger.warning(f"Failed to search mailbox: {mailbox}")
        return

    uids: List[bytes] = data[0].split()
    folder: Path = config.SAVE_DIR / label
    folder.mkdir(parents=True, exist_ok=True)

    logger.info(f"Got {len(uids)} messages")
    for uid in uids:
        uid_str = uid.decode()

        typ, msg_data = mail.uid("fetch", uid, "(RFC822)")
        if typ == "OK":
            raw_msg: bytes = msg_data[0][1]
            # email = save_eml(uid_str, raw_msg, folder)
        else:
            logger.warning(f"Failed to fetch message UID {uid_str}")


def sync_all():
    logger.info(72 * "=")
    logger.info(f"Syncing account '{config.IMAP.LABEL}")

    mail = connect_to_imap(config.IMAP)

    sync_mailbox(mail, config.IMAP.LABEL, config.IMAP.MAILBOX)

    mail.logout()

    logger.info(f"--> Done syncing account '{config.IMAP.LABEL}")
