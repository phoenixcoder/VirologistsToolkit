from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch
from managers import XlManager
from readers import XlReader

class TestXlManager(XlManager):
    @patch("readers.XlReader")
    @patch("openpyxl.worksheet.worksheet.Worksheet")
    @patch("openpyxl.Workbook")
    @patch("managers.load_workbook")
    def testReadResultsFromWorkbook(self, testload_workbook,
        testWorkbook, testWorksheet, testReader):
        testFilePath = "Test Output Path"
        testNames = ["Sheet 1", "Sheet 2"]
        testWorkbook.get_sheet_by_name.return_value = testWorksheet
        testload_workbook.return_value = testWorkbook
        testWorkbook.get_sheet_names.return_value = testNames

        testManager = XlManager()
        testManager.readResultsFromWorkbook(testFilePath, testReader)

        testload_workbook.assert_called_once_with(testFilePath)
        testWorkbook.get_sheet_names.assert_called_once_with()

        for testName in testNames:
            testWorkbook.get_sheet_by_name \
                .assert_any_call(testName)
            testReader.read.assert_any_call(testWorksheet)
