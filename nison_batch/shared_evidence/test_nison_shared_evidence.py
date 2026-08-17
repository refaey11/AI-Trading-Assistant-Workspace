import unittest
from nison_shared_evidence import *

class TestNisonSharedEvidence(unittest.TestCase):
    def test_0039_confluence_never_creates_direction(self):
        r = confluence_evidence([EvidenceEvent('trend',1,'bullish'), EvidenceEvent('volume',2,'bullish')])
        self.assertTrue(r['available']); self.assertEqual(r['direction'], 'neutral')

    def test_0040_cluster_is_evidence_only(self):
        r = cluster_evidence([EvidenceEvent('hammer',1,'bullish'), EvidenceEvent('engulfing',2,'bullish')])
        self.assertTrue(r['available']); self.assertEqual(r['direction'], 'neutral')

    def test_0041_requires_confirmation_after_touch(self):
        r = trendline_confirmation(EvidenceEvent('trendline_touch',10), EvidenceEvent('candle',9,'bullish'))
        self.assertFalse(r['available'])
        r = trendline_confirmation(EvidenceEvent('trendline_touch',10), EvidenceEvent('candle',11,'bullish'))
        self.assertTrue(r['available']); self.assertEqual(r['direction'], 'bullish')

    def test_0042_requires_level_test_before_confirmation(self):
        r = support_resistance_confirmation(EvidenceEvent('support_test',10), EvidenceEvent('candle',11,'bullish'))
        self.assertTrue(r['available'])

    def test_0043_requires_break_return_confirmation_order(self):
        good = false_breakout_confirmation(EvidenceEvent('spring',10), EvidenceEvent('return_inside_range',11), EvidenceEvent('candle',12,'bullish'))
        bad = false_breakout_confirmation(EvidenceEvent('spring',10), EvidenceEvent('return_inside_range',12), EvidenceEvent('candle',11,'bullish'))
        self.assertTrue(good['available']); self.assertFalse(bad['available'])

    def test_0044_requires_successful_retest(self):
        good = polarity_confirmation(EvidenceEvent('level_break',10), EvidenceEvent('successful_retest',12), EvidenceEvent('candle',13,'bearish'))
        bad = polarity_confirmation(EvidenceEvent('level_break',10), EvidenceEvent('failed_retest',12), EvidenceEvent('candle',13,'bearish'))
        self.assertTrue(good['available']); self.assertFalse(bad['available'])

    def test_no_lookahead_is_enforced(self):
        r = polarity_confirmation(EvidenceEvent('level_break',10), EvidenceEvent('successful_retest',12), EvidenceEvent('candle',11,'bullish'))
        self.assertFalse(r['available'])

if __name__ == '__main__':
    unittest.main()
