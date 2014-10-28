from unittest import TestCase
from unittest.mock import MagicMock, PropertyMock, Mock, patch, DEFAULT

from structures import DNA, SubstitutionMatrix
from readers import ObservedExpectedMatricesReader
from openpyxl.worksheet.worksheet import Worksheet

class TestObservedExpectedMatricesReader(TestCase):
    validDiagonalVal = 0
    validNonDiagonalVal = 1
    validRawDataWithDNAHeaders = None

    def setUp(self):
        self.validHeaders = ["Header 1", "Header 2", "Header 3"]
        self.validRawDataWithHeaders = self \
            .generateValidRawDataWithHeaders()

    @patch('structures.SubstitutionMatrix')
    @patch('structures.SubstitutionMatrix')
    @patch('openpyxl.worksheet.worksheet.Worksheet')
    def testRead(self, mockWorksheet, mockObservedMatrix,
        mockExpectedMatrix):
        mockBases = Mock()

        testTitle = "Test Title"
        mockWorksheetTitle = PropertyMock(return_value = testTitle)
        type(mockWorksheet).title = mockWorksheetTitle

        testResult = (mockObservedMatrix, mockExpectedMatrix)
        testReader = ObservedExpectedMatricesReader(mockBases)
        testReader._validateHeaders = MagicMock(return_value = True)
        testReader._readAndValidateSubstitutionValues = \
            MagicMock(return_value = testResult)

        testReader.read(mockWorksheet)

        self.assertEquals(testReader.matricesDictionary[testTitle],
            testResult, "Matrices dictionary value must be equal to the"
            + "test result.")

        testReader._validateHeaders \
            .assert_any_call(18, 1, mockWorksheet)
        testReader._validateHeaders \
            .assert_any_call(18, 7, mockWorksheet)
        self.assertEquals(testReader._validateHeaders.call_count, 2,
            "Header validation must have been called exactly twice.")
        testReader._readAndValidateSubstitutionValues \
            .assert_called_once_with(mockWorksheet)

        mockWorksheetTitle.assert_called_once_with()

    @patch('openpyxl.worksheet.worksheet.Worksheet')
    def test_ValidateHeaders(self, mockWorksheet):
        testStartRowIndex = 0
        testStartColIndex = 0
        testHeaders = self.validHeaders

        mockKeys = MagicMock()
        mockKeys.__iter__.return_value = testHeaders
        mockMembers = Mock()
        mockMembers.keys.return_value = mockKeys

        mockBase = Mock()
        pMockMembers = PropertyMock(return_value = mockMembers)
        type(mockBase).__members__ = pMockMembers

        mockWorksheet.cell = MagicMock(side_effect =
            self.getValidHeaderValue)

        testReader = ObservedExpectedMatricesReader(mockBase)
        testReader._validateHeaders(testStartRowIndex,
            testStartColIndex, mockWorksheet)

        mockKeys.__iter__.assert_called_once_with()
        mockMembers.keys.assert_called_once_with()
        pMockMembers.assert_called_once_with()
        mockMembers.keys.assert_called_once_with()

        testFullHeaders = [" "]
        testFullHeaders.append(self.validHeaders)
        for index in range(len(testFullHeaders)):
            mockWorksheet.cell.assert_any_call(row = testStartRowIndex
                + index, column = testStartColIndex)
            mockWorksheet.cell.assert_any_call(row = testStartRowIndex,
                column = testStartColIndex + index)

    def getValidHeaderValue(self, row, column):
        testHeaders = [" "]
        testHeaders.append(self.validHeaders)
        result = None
        if row == 0:
            result = testHeaders[column]
        else:
            result = testHeaders[row]
        return result

    def getValidRawValueAt(self, row, column):
        return self.validRawDataWithHeaders[row][column]

    def generateValidRawDataWithHeaders(self):
        data = 1
        rawData = []
        rowHeader = [" "]
        rowHeader.append(self.validHeaders)
        rawData.append(rowHeader)
        for index, header in enumerate(self.validHeaders):
            newRow = []
            newRow.append(header)
            for col in range(len(self.validHeaders)):
                if col == index:
                    newRow.append(0)
                else:
                    newRow.append(data)
            rawData.append(newRow)
        self.validRawDataWithHeaders = rawData

        return rawData

    @patch('readers.SubstitutionMatrix')
    @patch('openpyxl.worksheet.worksheet.Worksheet')
    def test_readAndValidateSubstitutionValues(self,
        mockWorksheet, mockSubstitutionMatrix):
        testStartRowIndex = 0
        testStartColIndex = 0

        mockBase = MagicMock()
        mockBase.__iter__.returen_value = self.validHeaders
        mockSubstitutionMatrix.incrementSubstitution = Mock()

        mockWorksheet.cell = MagicMock(side_effect =
            self.getValidRawValueAt)

        testReader = ObservedExpectedMatricesReader(mockBase)
        testReader._convertToFloat = Mock(side_effect =
            self.convertToFloat)
        testReader._readAndValidateSubstitutionValues(
            testStartRowIndex, testStartColIndex, mockWorksheet)

        squareSize = len(mockBase)
        for testRi, testSrc in enumerate(mockBase):
            for testCi, testDest in enumerate(mockBase):
                testAdjRi = testRi + 1
                testAdjCi = testCi + 1
                testAmount = self.getValieRawValueAt(testAdjRi,
                    testAdjCi)
                testReader._convertToFloat.assert_any_call(testAmount)
                mockWorksheet.cell \
                    .assert_any_call(row = testAdjRi,
                    column = testAdjCi)
                mockSubstitutionMatrix.incrementSubstitution \
                    .assert_any_call(testSrc, testDest, testAmount)

    @patch('readers.SubstitutionMatrix')
    @patch('openpyxl.worksheet.worksheet.Worksheet')
    def test_readAndValidateWorksheet(self, mockWorksheet,
        mockSubstitutionMatrix):
        mockBase = Mock()
        testReader = ObservedExpectedMatricesReader(mockBase)
        testReader._readAndValidateSubstitutionValues = \
            Mock(return_value = mockSubstitutionMatrix)

        testResult = testReader._readAndValidateWorksheet(mockWorksheet)

        testReader._readAndValidateSubstitutionValues.assert_any_call(18,
            1, mockWorksheet)
        testReader._readAndValidateSubstitutionValues.assert_any_call(18,
            7, mockWorksheet)

        self.assertEquals(tuple([mockSubstitutionMatrix,
            mockSubstitutionMatrix]), testResult, "Results must be " + \
            "the same.")

    def convertToFloat(self, target):
        result = 0.0
        try:
            result = float(target)
        except ValueError:
            raise ValueError()

        return result
