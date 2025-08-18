import unittest

from stalwart_backup.Email import Email
from stalwart_backup.imap_sync import connect_to_imap
from stalwart_backup.config import config


class TestIMAPSync(unittest.TestCase):
    def test_error(self):
        imap_conf = config.IMAP_LIST[1]
        mail = connect_to_imap(imap_conf)

        typ, data = mail.select(imap_conf.MAILBOX, readonly=True)

        uid = b"14142"
        typ, msg_data = mail.uid("fetch", uid, "(RFC822)")
        raw_msg: bytes = msg_data[0][1]
        mail = Email.from_bytes(raw_msg)


if __name__ == "__main__":
    a = TestIMAPSync()

    a.test_error()
