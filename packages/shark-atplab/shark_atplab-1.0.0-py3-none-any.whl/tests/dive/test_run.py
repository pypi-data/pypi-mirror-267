import unittest

from shark_atplab.dive.run import run_normal, run_sparse, run_collapsed


class TestRun(unittest.TestCase):
    def test_run__normal(self):
        normal_score = run_normal(
            k=5,
            sequence1='MKSMKSSSSTGWGWGTGWHFMKSSSSTGWGWGMKSTLKNGTEQMKSTGWHF',
            sequence2='MKSTGWHFMKSSSSTGMKSSSSTGWGWGWGWGMKSTLKNGTEQMKSSSSTGWGWGMKSTGWHFMKSTGWHF',
            threshold=0.5
        )
        self.assertIsNotNone(normal_score)
        self.assertGreaterEqual(normal_score, 0)
        self.assertLessEqual(normal_score, 1)

    def test_run__sparse(self):
        sparse_score = run_sparse(
            k=5,
            sequence1='MKSMKSSSSTGWGWGTGWHFMKSSSSTGWGWGMKSTLKNGTEQMKSTGWHF',
            sequence2='MKSTGWHFMKSSSSTGMKSSSSTGWGWGWGWGMKSTLKNGTEQMKSSSSTGWGWGMKSTGWHFMKSTGWHF'
        )
        self.assertIsNotNone(sparse_score)
        self.assertGreaterEqual(sparse_score, 0)
        self.assertLessEqual(sparse_score, 1)

    def test_run__collapsed(self):
        collapsed_score = run_collapsed(
            k=3,
            sequence1='MKSMKSSSSTGWGWGTGWHFMKSSSSTGWGWGMKSTLKNGTEQMKSTGWHF',
            sequence2='MKSTGWHFMKSSSSTGMKSSSSTGWGWGWGWGMKSTLKNGTEQMKSSSSTGWGWGMKSTGWHFMKSTGWHF'
        )
        self.assertIsNotNone(collapsed_score)
        self.assertGreaterEqual(collapsed_score, 0)
        self.assertLessEqual(collapsed_score, 1)

    def test_updated_run_sparse(self):
        sparse_score = run_normal(
            k=2,
            threshold=0,
            sequence1='TYSGGGGP',
            sequence2='TYSGGGGP'
        )
        self.assertIsNotNone(sparse_score)
        self.assertGreaterEqual(sparse_score, 0)
        self.assertLessEqual(sparse_score, 1)


if __name__ == '__main__':
    unittest.main()
