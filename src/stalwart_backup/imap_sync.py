import imaplib
from pathlib import Path
from typing import List
import mailbox
from email.parser import BytesParser
from email import policy

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


def sync_mailbox(mail: imaplib.IMAP4_SSL):
    """
    Download and process emails

    Args:
        mail: Handler to the IMAP server, got with a call to `connect_to_imap`

    """
    label = config.IMAP.LABEL
    folder_name = config.IMAP.MAILBOX

    try:
        typ, data = mail.select(folder_name, readonly=True)
    except Exception:
        typ = "NO"
    if typ != "OK":
        logger.warning(f"Failed to select folder_name: {folder_name}")
        return

    filter = "ALL"
    typ, data = mail.uid("search", None, filter)
    if typ != "OK":
        logger.warning(f"Failed to search folder_name: {folder_name}")
        return

    uids: List[bytes] = data[0].split()
    # folder: Path = config.SAVE_DIR / label
    # folder.mkdir(parents=True, exist_ok=True)

    destination = mailbox.mbox(config.MBOX_FILE)
    destination.lock()

    logger.info(f"Got {len(uids)} messages")
    for uid in uids:
        uid_str = uid.decode()
        # eml_path = folder / f"{uid_str}.eml"

        typ, msg_data = mail.uid("fetch", uid, "(RFC822)")
        if typ == "OK":
            raw_msg: bytes = msg_data[0][1]
            # email = save_eml(uid_str, raw_msg, folder)
            msg = BytesParser(policy=policy.default).parsebytes(raw_msg)
            destination.add(mailbox.MHMessage(msg))
        else:
            logger.warning(f"Failed to fetch message UID {uid_str}")

    destination.flush()
    destination.unlock()


def sync_all():
    logger.info(72 * "=")
    logger.info(f"Syncing account '{config.IMAP.LABEL}")

    mail = connect_to_imap(config.IMAP)

    sync_mailbox(mail)

    mail.logout()

    logger.info(f"--> Done syncing account '{config.IMAP.LABEL}")
