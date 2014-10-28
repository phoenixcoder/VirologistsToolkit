from enum import IntEnum
from enum import unique

@unique
class DNA(IntEnum):

    """Enumerates the ACGT nucleotides for DNA."""

    A = 0
    C = 1
    G = 2
    T = 3

class SubstitutionMatrix:

    """Represents a nucleotide substitution matrix for DNA or RNA bases. 
    
    Primarily imposes the following rule that a nucleotide cannot
    have a substitution rate higher than 0 with itself.  
    """

    def __init__(self, nucleobaseType):
        """Specifies the nucleotide bases the matrix represents: DNA/RNA.

        :param nucleobase: Enum of type DNA/RNA.
        """
        self.nucleobaseType = nucleobaseType
        self.nucleobaseLength = len(list(nucleobaseType))
        self.substitutionMatrix = \
            [[0 for x in range(self.nucleobaseLength)] \
            for x in range(self.nucleobaseLength)]

    def incrementSubstitution(self, sourceBase, destinationBase, amount):
        """Increments the entry at position source and destination by
        the amount passed.

        The entry at (source, destination) will not be incremented by the
        amount if source is equal to the destination.

        :param sourceBase:      Enum instance of the nucleotide source.
        :param destinationBase: Enum instance of the nucleotide
                                destination.
        :param amount:          Amount to increment the entry by.
        """
        if sourceBase != destinationBase:
            self.substitutionMatrix[sourceBase] \
                [destinationBase] = amount

    def getCopy(self):
        """Returns a defensive copy of the substitution matrix.
        
        :returns: Defensive copy of the substitution matrix.
        """
        defensiveCopy = []
        for source in self.substitutionMatrix:
            defensiveSource = []
            for destination in source:
                defensiveSource.append(destination)
            defensiveCopy.append(defensiveSource)
        return defensiveCopy
