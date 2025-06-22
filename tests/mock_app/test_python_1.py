import unittest
from time import sleep
from mock_app.logger import write_log


class TestPythonOne(unittest.TestCase):

    def test_python_one(self) -> None:
        write_log('[pytest:test_python_one] start')
        sleep(1)
        write_log('[pytest:test_python_one] stop')
