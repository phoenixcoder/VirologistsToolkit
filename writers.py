from abc import ABCMeta, abstractmethod
from structures import DNA, SubstitutionMatrix
from datetime import date

class XlWriter:
    
    """Encapsulates the data and the means to write it.

    This ports the method to write structure data to a given workbook.
    The method is defined by its subclass.
    """

    @abstractmethod
    def write(self, workbook):
        """Writes the structured data to a workbook.

        Subclasses define where data is written in the workbook.
        """
        pass

class SubstitutionMatrixDataWriter(XlWriter):

    """Writes SubstitutionMatrix data to file."""

    headerRowIndex = 1
    headerColIndex = 1
    currRowIndex = 2

    def __init__(self, subjectHeaderName, validSubjects,
        invalidSubjects, nucleobaseType = DNA):
        self.subjectHeaderName = subjectHeaderName
        self.validSubjects = validSubjects
        self.invalidSubjects = invalidSubjects
        self.nucleobaseType = nucleobaseType

    def write(self, workbook):
        """Writes the data associated with this writer to the workbook.

        Defines the structure of the headers and the data within the
        workbook across worksheets.  It expects the validSubjects
        attribute to contain a dictionary with a 1-1 association of the
        subject name to the subject's SubstitutionMatrix. This
        SubstitutionMatrix should contain the information to be written
        to file.

        :param workbook: Workbook the data is to be written to.
        """
        # TODO Task #3: Handle case for Worksheets of Same Name
        # TODO Allow for multiple results under a single workbook.
        # TODO Write out invalid subjects in a worksheet.
        worksheet = workbook.create_sheet(title = "Results")
        self._writeHeaders(worksheet)

        subjects = self.validSubjects
        for subjectName in subjects.keys():
            self._writeSubject(str(subjectName), subjects[subjectName],
                worksheet)

    def _writeHeaders(self, worksheet):
        """Writes the header row to the given worksheet.

        Currently, the default header row is defined as:
        Virus | A -> C | A -> G | A -> T | C -> A | C -> G | etc.

        It is defined as all combinations of nucleobase pairs unless the
        second pair is the same as the first.
        """
        nucleobaseType = self.nucleobaseType
        headerRowIndex = self.headerRowIndex
        headerColIndex = self.headerColIndex
        colIndex = headerColIndex + 1
        worksheet.cell(row = headerRowIndex, column =
            headerColIndex).value = "Virus"
        for source in nucleobaseType:
            for dest in nucleobaseType:
                if source != dest:
                    worksheet.cell(row = headerRowIndex,
                        column = colIndex).value = str(source) + \
                            " -> " + str(dest)
                    colIndex = colIndex + 1

    def _writeSubject(self, subjectName, biasSubstitutionMatrix,
        worksheet):
        """Writes the substitution matrix to the subject's row.

        :param subjectName:            Name of the subject to be written.
        :param biasSubstitutionMatrix: Substitution matrix containing
                                       the data to be written.
        "param worksheet:              Name of the worksheet the data is
                                       to be written to.
        """
        biasValueMatrix = biasSubstitutionMatrix.getCopy()
        nucleobaseType = self.nucleobaseType
        headerColIndex = self.headerColIndex
        currRowIndex = self.currRowIndex

        worksheet.cell(row = currRowIndex, column =
            headerColIndex).value = subjectName

        colIndex = headerColIndex + 1
        for source in nucleobaseType:
            for dest in nucleobaseType:
                if source != dest:
                    amount = biasValueMatrix[source][dest]
                    worksheet.cell(row = currRowIndex, column =
                        colIndex).value = amount
                    colIndex = colIndex + 1

        self.currRowIndex = currRowIndex + 1
