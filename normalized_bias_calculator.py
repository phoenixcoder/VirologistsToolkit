from nucleotide_calculations import NucleotideSubstitutionBiasCalculator

class NormalizedSubstitutionBiasCalculator(NucleotideSubstitutionBiasCalculator):

    """Container for the normalized substitution bias calculation.

    Used for portability of the formula:

    [ (Observed Value) - (Expected Value) ] / (Expected Value)
    """

    def _customCalculation(self, observed, expected):
        """Returns a normalized substitution bias."""
        result = (observed - expected) / expected
        return result
