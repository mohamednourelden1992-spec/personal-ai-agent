import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from personal_agent.memory import MemoryStore


class MemoryStoreTests(unittest.TestCase):
    def test_remember_and_search(self):
        with tempfile.TemporaryDirectory() as directory:
            store = MemoryStore(str(Path(directory) / "test.db"))
            store.remember("I prefer Python for backend projects")
            self.assertEqual(store.search("Python"), ["I prefer Python for backend projects"])


if __name__ == "__main__":
    unittest.main()
