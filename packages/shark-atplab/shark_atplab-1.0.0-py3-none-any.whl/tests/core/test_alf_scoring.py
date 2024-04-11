import unittest

from shark_atplab.core.alf_scoring import get_google_distance_score


class TestAlfScoring(unittest.TestCase):
    def test_get_google_distance_score__wrong_k(self):
        score = get_google_distance_score(
            sequence1='MKSTGWHF',
            sequence2='MKSSSSTGWGWG',
            k=7
        )
        self.assertIsNone(score)

    def test_get_google_distance_score__positive(self):
        score = get_google_distance_score(
            sequence1='MKSTGWHF',
            sequence2='MKSSSSTGWGWG',
            k=2
        )
        self.assertIsNotNone(score)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 1)


if __name__ == '__main__':
    unittest.main()
