# https://github.com/stalwartlabs/stalwart/discussions/1777

import re
import os
import mailbox
import email
from email.utils import parsedate_tz, mktime_tz
import time

from stalwart_backup import logger
from stalwart_backup.config import config
from stalwart_backup.imap_sync import connect_to_imap


def delete_all_emails():
    # Connect to server and login
    mail = connect_to_imap(config.IMAP)

    # Select the mailbox (e.g., "INBOX")
    mail.select("INBOX")

    # Search for all messages
    typ, data = mail.search(None, "ALL")
    if typ != "OK":
        print("Error searching mailbox.")
        return

    for num in data[0].split():
        # Mark each email for deletion
        mail.store(num, "+FLAGS", r"(\Deleted)")

    # Permanently remove all emails marked \Deleted
    mail.expunge()

    mail.close()
    mail.logout()
    print("All emails deleted from INBOX.")


eml_regex = re.compile(".*\\.eml")


def create_mbox_file():
    output_mbox_file = "yann.mbox"
    maildir_path = "Maildir"

    if os.path.exists(output_mbox_file):
        print(f"WARN: Deleting existing mbox: {output_mbox_file}")
        os.remove(output_mbox_file)

    # destination = mailbox.mbox(output_mbox_file)
    destination = mailbox.Maildir(maildir_path, create=True)

    for root, dirs, files in os.walk("emails/yann@johncloud.fr", topdown=True):
        eml_files = list(filter(eml_regex.match, files))
        for eml_file in eml_files:
            eml_file_path = os.path.join(root, eml_file)
            with open(eml_file_path, "rb") as f:
                msg = email.message_from_binary_file(f)

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
                    logger.warning(f"No date found for {eml_file}")
            else:
                mbox_msg.set_from(msg.get("From", "unknown"))
                logger.warning(f"No date found for {eml_file}")

            destination.add(mbox_msg)

    destination.flush()


delete_all_emails()
# create_mbox_file()
