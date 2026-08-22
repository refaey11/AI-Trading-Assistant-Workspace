import unittest
from murphy_0018_0019_runtime_v1 import WedgeEvidence, evaluate_0018, evaluate_0019, NOT_EVALUABLE, NO_SIGNAL, BULLISH, BEARISH

class Murphy0018_0019RuntimeTests(unittest.TestCase):
    def test_0018_bullish_on_falling_wedge_upside_breakout(self):
        self.assertEqual(evaluate_0018(WedgeEvidence('FALLING_WEDGE','UPSIDE',True,True)), BULLISH)
    def test_0018_no_signal_on_wrong_breakout(self):
        self.assertEqual(evaluate_0018(WedgeEvidence('FALLING_WEDGE','DOWNSIDE',True,True)), NO_SIGNAL)
    def test_0019_bearish_on_rising_wedge_downside_breakout(self):
        self.assertEqual(evaluate_0019(WedgeEvidence('RISING_WEDGE','DOWNSIDE',True,True)), BEARISH)
    def test_0019_no_signal_on_wrong_breakout(self):
        self.assertEqual(evaluate_0019(WedgeEvidence('RISING_WEDGE','UPSIDE',True,True)), NO_SIGNAL)
    def test_missing_geometry_is_not_evaluable(self):
        self.assertEqual(evaluate_0018(WedgeEvidence('FALLING_WEDGE','UPSIDE',False,True)), NOT_EVALUABLE)
    def test_missing_breakout_is_not_evaluable(self):
        self.assertEqual(evaluate_0019(WedgeEvidence('RISING_WEDGE','DOWNSIDE',True,False)), NOT_EVALUABLE)

if __name__ == '__main__':
    unittest.main()
