import unittest
from murphy_0018_0019_runtime_v1 import (
    WedgeGeometryEvidence, evaluate_0018, evaluate_0019,
    PASS, FAIL, NOT_EVALUABLE,
)

class Murphy0018_0019RuntimeTests(unittest.TestCase):
    def test_0018_passes_when_converging_and_both_slopes_negative(self):
        e = WedgeGeometryEvidence(True, -0.2, -0.1, True)
        self.assertEqual(evaluate_0018(e), PASS)

    def test_0018_fails_when_not_converging(self):
        e = WedgeGeometryEvidence(False, -0.2, -0.1, True)
        self.assertEqual(evaluate_0018(e), FAIL)

    def test_0019_passes_when_converging_and_both_slopes_positive(self):
        e = WedgeGeometryEvidence(True, 0.1, 0.2, True)
        self.assertEqual(evaluate_0019(e), PASS)

    def test_0019_fails_when_not_converging(self):
        e = WedgeGeometryEvidence(False, 0.1, 0.2, True)
        self.assertEqual(evaluate_0019(e), FAIL)

    def test_missing_geometry_is_not_evaluable(self):
        e = WedgeGeometryEvidence(True, -0.2, -0.1, False)
        self.assertEqual(evaluate_0018(e), NOT_EVALUABLE)

    def test_missing_slope_is_not_evaluable(self):
        e = WedgeGeometryEvidence(True, None, 0.2, True)
        self.assertEqual(evaluate_0019(e), NOT_EVALUABLE)

if __name__ == '__main__':
    unittest.main()
