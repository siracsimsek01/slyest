import unittest

from app.core.session import SessionManager
import os
from PyPDF2 import PdfReader

class TestSessionExport(unittest.TestCase):
    def __init__(self):
        self.session_manager = SessionManager()
        self.name = "John"
        self.items = ['First Item', 'Second Item', 'Third Item']

    def run_all_tests(self):
        self.test_create_folder_and_txt_file()
        self.test_written_inputs_are_accurate()
        self.test_pdf_file_exists()
        self.test_pdf_content_are_accurate()
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
    
    def test_pdf_file_exists(self):
        file_name = self.session_manager.export_history("pdf", self.name, self.items)
        self.assertTrue(os.path.exists(file_name))
        print('>> Test Func: export PDF file, Test: A PDF file is created, Result: Success')

    def test_pdf_content_are_accurate(self):
        file_name = self.session_manager.export_history("pdf", self.name, self.items)
        reader = PdfReader(file_name)
        all_text = ""
        for page in reader.pages:
            all_text += page.extract_text() or ""
        print(all_text)
        for text in self.items:
            if text not in all_text:
                raise AssertionError(f"Expected text '{text}' not found in PDF.")
        print('>> Test Func: export PDF file, Test: Items are written correctly, Result: Success')

test_suite = TestSessionExport()
test_suite.run_all_tests()