import unittest

from app.core.session import SessionManager
import os

class TestSessionExport(unittest.TestCase):
    def __init__(self):
        self.session_manager = SessionManager()
        self.name = "John"
        self.items = ['First Item', 'Second Item', 'Third Item']

    def run_all_tests(self):
        self.test_create_folder_and_txt_file()
        self.test_written_inputs_are_accurate()
        print("All tests ran successfully!")

    def test_create_folder_and_txt_file(self):
        filepath = self.session_manager.export_history("txt", self.name, self.items)
        self.assertTrue(os.path.exists("HistoryFiles"))
        self.assertTrue(os.path.exists(filepath))
        print('>> Test Func: export text file, Test: A folder and file is created, Result: Success')

    def test_written_inputs_are_accurate(self):
        filepath = self.session_manager.export_history("txt", self.name, self.items)
        with open(filepath, "r", encoding="utf-8") as file:
            lines = file.read().splitlines()
            lines = [line[3:] for line in lines]
        assert lines == self.items
        print('>> Test Func: export text file, Test: Items are correctly written, Result: Success')

test_suite = TestSessionExport()
test_suite.run_all_tests()