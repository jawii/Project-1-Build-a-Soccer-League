import unittest
import worklog
import datetime

from unittest.mock import patch

class LogTests(unittest.TestCase):
    def test_ask_for_workers_name(self):
        with unittest.mock.patch('builtins.input', return_value="yes"):
            self.assertIsNotNone(worklog.ask_worker_name())


    def test_ask_for_task_name(self):
        with unittest.mock.patch('builtins.input', return_value="taskname"):
            self.assertIsNotNone(worklog.ask_task_name())


    def test_ask_for_date(self):
        with unittest.mock.patch('builtins.input', return_value="12/12/1988 12:20"):
            self.assertIsNotNone(worklog.ask_work_date())


    def test_ask_for_additional_notes(self):
        with unittest.mock.patch('builtins.input', return_value="Notenotesnotesnotes"):
            self.assertIsNotNone(worklog.ask_for_notes_to_task())

    def test_asko_for_time_spend_on_task(self):
        with unittest.mock.patch('builtins.input', return_value="120"):
            self.assertIsNotNone(worklog.ask_for_time_spend_on_task())

if __name__ == '__main__':
    unittest.main()