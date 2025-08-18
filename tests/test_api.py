import unittest

from stalwart_backup.imap_sync import sync_all


class TestIMAPSync(unittest.TestCase):
    def test_sync_all(self):
        sync_all()


if __name__ == "__main__":
    a = TestIMAPSync()

    a.test_sync_all()
