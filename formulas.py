from abc import ABCMeta
from abc import abstractmethod

class Formula:
    
    """Provides a uniform interface for calculating the bias.

    There can be multiple layouts of the input and/or multiple ways to
    calculate the bias including a provision for the original
    Chi-squared test.  So strategy pattern is used to accomodate the
    multiple avenues for which a calculation can be done.
    """

    __metaclass__ = ABCMeta

    def __validate(self, input):
        """Validates the input is not None and can be converted to long.

        :param input: Non-None float value or a string that can be
                      converted to a long value.
        :returns:     True, if valid.  False, otherwise.
        """
        valid = (input is not None) \
            and self.__validateFloatInput(input)
        return valid

    def __validateFloatInput(self, input):
        """Validates number or string input for real number conversion.
        
        :param input: float value or string convertable to float value.
        :returns:     True, if convertable.  False, otherwise.
        """
        result = False
        try:
            float(input)
            result = True
        except ValueError:
            pass

        return result

    def calculate(self, observed, expected):
        """Applies the formula to the expected and observed values.

        Performs a validation before running the custom calculation
        implemented by the subclass.

        :param observed: Real number of observed nucleotide 
                         substitutions.
        :param expected: Non-zero Real number of expected nucleotide
                         substitutions.
        :returns:        Number or None representing the final result 
                         of the calculations based on the observed and
                         expected nucleotide substitutions. If either 
                         the observed or expected value is invalid, the
                         return is simply None.
        """
        result = None
        valid = self.__validate(observed) \
            and self.__validate(expected) \
            and expected != 0
        if valid:
            result = self._calculation(float(observed),
                float(expected))
        return result

    @abstractmethod
    def _calculation(self, observed, expected):
        """See :func: `calculate`"""
        pass

class NormalizedSubstitutionBiasFormula(Formula):

    """Container for the normalized substitution bias formula.

    Used for portability of the formula:

    [ (Observed Value) - (Expected Value) ] / (Expected Value)
    """

    def _calculation(self, observed, expected):
        """Returns the result of the normalized substitution bias."""
        result = (observed - expected) / expected
        return result
