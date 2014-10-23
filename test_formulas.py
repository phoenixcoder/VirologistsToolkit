from formulas import NormalizedSubstitutionBiasFormula
from unittest import TestCase

class TestNormalizedSubstitutionBiasFormula(TestCase):
    __testNormalizedSubstitutionBiasFormula = None

    def setUp(self):
        self.__testNormalizedSubstitutionBiasFormula = \
            NormalizedSubstitutionBiasFormula()

    def tearDown(self):
        self.__testNormalizedSubstitutionBiasFormula = None

    def test_NotNoneOnCreation(self):
        self.assertIsNotNone(self \
            .__testNormalizedSubstitutionBiasFormula,
            """Test instance must not be None.""")

    def test_CalculateWithValidValues(self):
        testMethod = self.__testNormalizedSubstitutionBiasFormula \
            .calculate
        errorMsg = """ \
        Bias must be equal to {0} with observed value {1} \
        and expected value {2}.  Result was: {3} \
        """

        observed = 2
        expected = 1
        result = testMethod(observed, expected)
        self.assertEqual(result, 1, errorMsg.format(1, observed,
            expected, result))

        observed = 0
        expected = 1
        result = testMethod(observed, expected)
        self.assertEqual(result, -1, errorMsg.format(-1, observed,
            expected, result))

        observed = -1
        expected = -2
        result = testMethod(observed, expected)
        self.assertEqual(result, -0.5, errorMsg.format(-0.5, observed,
            expected, result))

    def test_CalculateWithInvalidValues(self):
        testMethod = self.__testNormalizedSubstitutionBiasFormula \
            .calculate

        observed = 1
        expected = 0
        result = testMethod(observed, expected)
        self.assertIsNone(result, """ \
        Bias must return None when the expected value is 0. \
        Result was: {0} \
        """.format(result))

        observed = "-"
        expected = 1
        result = testMethod(observed, expected)
        self.assertIsNone(result, """ \
        Bias must return None when the observed value is '-'. \
        Result was: {0} \
        """.format(result))

        observed = 1
        expected = "-"
        result = testMethod(observed, expected)
        self.assertIsNone(result, """ \
        Bias must return None when the expected value is '-'. \
        Result was: {0} \
        """.format(result))

        observed = "-"
        expected = "-"
        result = testMethod(observed, expected)
        self.assertIsNone(result, """ \
        Bias must return None when the observed and expected value is \
        '-'. Results for observed and expected, respectively: {0}, {1} \
        """.format(observed, expected))

if __name__ == "__main__":
    unittest.main()
