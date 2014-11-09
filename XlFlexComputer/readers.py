from abc import ABCMeta, abstractmethod
from structures import SubstitutionMatrix, DNA

class XlReader:
    """Behaves as a custom targeter of raw data in the Excel sheet.

    This allows the developer or even the user to create custom
    extraction classes for retrieving different types of data from
    within a worksheet.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def read(self, worksheet):
        """Reads raw data from a worksheet.

        Subclasses define what data is extracted and from where in the
        context of the worksheet.
        """
        pass

class ObservedExpectedMatricesReader(XlReader):

    """Extracts pair of observed & expected substitution matrices."""

    def __init__(self, nucleobaseType = DNA,
        omStartingRi = 18,
        omStartingCi = 1, # Worksheets start from 1.
        emStartingRi = 18,
        emStartingCi = 7):
        self.matricesDictionary = dict()
        self.invalidSheets = []
        self.nucleobaseType = nucleobaseType
        self.omStartingRi = omStartingRi
        self.omStartingCi = omStartingCi
        self.emStartingRi = emStartingRi
        self.emStartingCi = emStartingCi

    def read(self, worksheet):
        """Validates and extracts worksheet's observed/expected matrices.

        Uses the instance's observed and expected starting row and 
        column to begin validating the matrix.

        The matrix must look like the following to be valid:
        _ |  A   C   G   T
        -------------------
        A |  -   N   N   N
          |
        C |  N   -   N   N
          |
        G |  N   N   -   N
          |
        T |  N   N   N   -
        **Notes: There are no gaps between columns and rows.  They are
        there for aesthetic purposes.

        [ Legend ]
         * Hyphens indicate '-', characters, or blanks.
         * N indicates numeral, numeric strings, or blanks.

        :param worksheet: Active worksheet object.
        :returns:         If worksheet contains valid observed and
                          expected matrices, then it will return a tuple
                          containing both.  Otherwise, it will return
                          None.
        """
        result = None
        omStartingRi = self.omStartingRi
        omStartingCi = self.omStartingCi
        emStartingRi = self.emStartingRi
        emStartingCi = self.emStartingCi
        if self._validateHeaders(omStartingRi, omStartingCi, worksheet) \
            and self._validateHeaders(self.emStartingRi,
            self.emStartingCi, worksheet):
            result = self._readAndValidateSubstitutionValues(worksheet)

        if result is not None:
            self.matricesDictionary[worksheet.title] = result

    def _validateHeaders(self, startRowIndex, startColIndex, worksheet):
        """Validates the row and column headers.

        Ensures all header values are in the nucleobase list or blank,
        and that they are unique within each row or column header.
        """
        result = True
        nucleobaseTypeMembers = self.nucleobaseType.__members__
        headerValues = list(nucleobaseTypeMembers.keys())
        headerValues.append(" ")
        for index in range(len(headerValues)):
            currRowValue = worksheet.cell(row = startRowIndex + index, 
                column = startColIndex)
            currColValue = worksheet.cell(row = startRowIndex,
                column = startColIndex + index)

            if currRowValue == currColValue \
                and currRowValue in headerValues:
                try:
                    headerValues.remove(currRowValue)
                except ValueError:
                    result = False
            else:
                result = False
                break

        return result

    def _readAndValidateWorksheet(self, worksheet):
        """Reads observed & expected matrix values.

        Assumes _validateHeaders has been run on the worksheet and is
        valid.  Validates the values as they're read.

        :returns: Tuple containing the observed and expected matrices
                  with associated substitution values. This returns None
                  if any of the substitution values are invalid.
        """
        result = None

        readMethod = self._readAndValidateSubstitutionValues
        observedMatrix = readMethod(self.omStartingRi,
            self.omStartingCi, worksheet)
        expectedMatrix = None

        if observedMatrix is not None:
            expectedMatrix = readMethod(self.emStartingRi,
                self.emStartingCi, worksheet)

        if expectedMatrix is not None:
            result = tuple([observedMatrix, expectedMatrix])

        return result

    def _readAndValidateSubstitutionValues(self, startingRowIndex,
        startingColIndex, worksheet):
        """Converts the raw data into a substitution matrix.

        :returns: Substitution matrix with a 1-1 mapping between the
                  entries in this matrix and the entries in the raw data.
        """

        nucleobaseType = self.nucleobaseType
        result = SubstitutionMatrix(nucleobaseType)
        for ri, source in enumerate(nucleobaseType):
            for ci, dest in enumerate(nucleobaseType):
                amount = worksheet.cell(row = startingRowIndex + ri + 1,
                    column = startingColIndex + ci + 1)
                try:
                    if ri == ci and \
                        self._convertToFloat(amount) != 0.0:
                        result = None
                        break
                    result.incrementSubstitution(source, dest,
                        self._convertToFloat(amount))
                except ValueError:
                    result = None
                    break

        return result

    def _convertToFloat(self, target):
        """Tries to convert the target to a float.

        Failure to convert it will result in a 0.0 value.
        """
        result = 0.0
        try:
            result = float(target)
        except ValueError:
            raise ValueError()

        return result
