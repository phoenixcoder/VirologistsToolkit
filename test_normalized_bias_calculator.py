from normalized_bias_calculator import NormalizedSubstitutionBiasCalculator
from unittest import TestCase

class TestNormalizedBiasCalculator(TestCase):
    __testNormalizedSubstitutionBiasCalculator = None

    def setUp(self):
        self.__testNormalizedSubstitutionBiasCalculator = \
            NormalizedSubstitutionBiasCalculator()

    def tearDown(self):
        self.__testNormalizedSubstitutionBiasCalculator = None

    def test_NotNoneOnCreation(self):
        self.assertIsNotNone(self \
            .__testNormalizedSubstitutionBiasCalculator, 
            """Test instance must not be None.""")

    def test_CalculateBiasWithValidValues(self):
        testMethod = self.__testNormalizedSubstitutionBiasCalculator \
            .calculateBias
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

    def test_CalculateBiasWithInvalidValues(self):
        testMethod = self.__testNormalizedSubstitutionBiasCalculator \
            .calculateBias

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
