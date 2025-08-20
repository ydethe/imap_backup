import email
import imaplib
import os
import shutil
import time
from typing import List
import mailbox
from email.utils import parsedate_tz, mktime_tz

from tqdm import tqdm

from .config import Config
from . import logger


def connect_to_imap(config: Config) -> imaplib.IMAP4_SSL:
    """Connect to the IMAP server

    Args:
        config: Connection information

    Returns:
        A object to interact with the IMAP server

    """
    mail = imaplib.IMAP4_SSL(config.SERVER, config.PORT)
    mail.login(config.USERNAME, config.PASSWORD)
    return mail


def sync_mailbox(config: Config, mail: imaplib.IMAP4_SSL):
    """
    Download and process emails

    Args:
        mail: Handler to the IMAP server, got with a call to `connect_to_imap`

    """
    folder_name = config.MAILBOX

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

    dest = config.MAILDIR_FOLDER / "Maildir"
    if dest.exists():
        logger.warning(f"Deleting existing Maildir: {dest}")
        shutil.rmtree(dest, ignore_errors=True)

    destination = mailbox.Maildir(dest, create=True)

    logger.info(f"Got {len(uids)} messages")
    for uid in tqdm(uids):
        uid_str = uid.decode()
        # eml_path = folder / f"{uid_str}.eml"

        typ, msg_data = mail.uid("fetch", uid, "(RFC822)")
        if typ == "OK":
            raw_msg: bytes = msg_data[0][1]
            msg = email.message_from_bytes(raw_msg)

            # Convert to mailbox.mboxMessage to keep metadata
            mbox_msg = mailbox.mboxMessage(msg)

            # Ensure the "Date" field from the email is preserved as delivery date
            if "date" in msg:
                try:
                    ts = mktime_tz(parsedate_tz(msg["date"]))
                    mbox_msg.set_from(from_=msg.get("From", "unknown"), time_=time.gmtime(ts))
                except Exception:
                    # fallback: no conversion, keep raw
                    mbox_msg.set_from(msg.get("From", "unknown"))
                    logger.warning(f"No date found for message {uid}")
            else:
                mbox_msg.set_from(msg.get("From", "unknown"))
                logger.warning(f"No date found for message {uid}")

            key = destination.add(mbox_msg)

            # Creation and modification date update
            msg_pth = dest / "new" / key
            os.utime(msg_pth, (ts, ts))

        else:
            logger.warning(f"Failed to fetch message UID {uid_str}")

    destination.flush()


def sync_all(config: Config):
    logger.info(72 * "=")
    logger.info(f"Syncing account '{config.USERNAME}")

    mail = connect_to_imap(config)

    sync_mailbox(config, mail)

    mail.logout()

    logger.info(f"--> Done syncing account '{config.USERNAME}")
