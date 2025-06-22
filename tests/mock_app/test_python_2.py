import unittest
from time import sleep
from mock_app.logger import write_log


class TestPythonTwo(unittest.TestCase):

    def test_python_two(self) -> None:
        write_log('[pytest:test_python_two] start')
        sleep(1)
        write_log('[pytest:test_python_two] stop')
