from nucleotide_data_structures import NucleotideSubstitutionMatrix, DNA
from unittest import TestCase

class TestNucleotideSubstitutionMatrix(TestCase):
    testNucleotideSubstitutionMatrix = None

    def setUp(self):
        self.testNucleotideSubstitutionMatrix = \
            NucleotideSubstitutionMatrix(DNA)

    def populateSubstitutionMatrix(self, matrix, nucleobaseType, step):
        for sourceBase in nucleobaseType:
            for destinationBase in nucleobaseType:
                matrix.incrementSubstitution(sourceBase, 
                destinationBase, step)

    def testIncrementSubstitutionAllEntries(self):
        substitutionMatrix = self.testNucleotideSubstitutionMatrix \
            .substitutionMatrix
        step = 1
        self.populateSubstitutionMatrix(
            self.testNucleotideSubstitutionMatrix, DNA, step)
        for ri, row in enumerate(substitutionMatrix):
            for ci, amount in enumerate(row):
                if ri != ci:
                    self.assertEquals(amount, step, \
                    "Entry must be equal to {0}.  ".format(step) + \
                    "Entry({0}, {1}) was {2}.".format(ri, ci, amount))
                else:
                    self.assertEquals(amount, 0, \
                    "Entry must be equal to 0.  " + \
                    "Entry({0}, {1}) was {2}.".format(ri, ci, amount))

    def testGetSubstitutionMatrixCopy(self):
        substitutionMatrix = self.testNucleotideSubstitutionMatrix \
            .substitutionMatrix
        step = 1
        self.populateSubstitutionMatrix(
            self.testNucleotideSubstitutionMatrix, DNA, step)
        defSubstitutionMatrix = self.testNucleotideSubstitutionMatrix \
            .getSubstitutionMatrixCopy()

        step = -1
        for ri, row in enumerate(defSubstitutionMatrix):
            for ci, col in enumerate(row):
                defSubstitutionMatrix[ri][ci] = step

        for rows in zip(substitutionMatrix, defSubstitutionMatrix):
            for pair in zip(rows[0], rows[1]):
                self.assertNotEquals(pair[0], pair[1],
                    "Changes in the defensive copy of the " + \
                    "substitution matrix must not change the " + \
                    "original matrix.")
