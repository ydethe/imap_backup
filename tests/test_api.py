import unittest
import json

import yaml
from yaml import BaseLoader

from imap_backup.imap_sync import sync_all
from imap_backup.config import Config


class TestIMAPSync(unittest.TestCase):
    def test_sync_all(self):
        with open("tests/dev.yml", "r") as f:
            dat = yaml.load(f, Loader=BaseLoader)
        config = Config.model_validate_json(json.dumps(dat))
        sync_all(config)


if __name__ == "__main__":
    a = TestIMAPSync()

    a.test_sync_all()
