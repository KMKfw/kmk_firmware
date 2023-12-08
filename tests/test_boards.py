import unittest
from glob import glob
from os import path
import subprocess


class TestBoards(unittest.TestCase):
    def test_import(self):
        mains = glob('boards/**/main.py', recursive=True)
        for f in mains:
            p = path.dirname(f)
            with self.subTest(p):
                subprocess.run(['python', '-m', 'tests.mock_board', p], check=True)
