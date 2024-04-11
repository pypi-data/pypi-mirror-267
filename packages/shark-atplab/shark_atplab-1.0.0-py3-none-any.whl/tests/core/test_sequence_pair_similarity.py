import unittest

from shark_atplab.core.utils import get_grantham_subs_matrix
from shark_atplab.core.sequence_pair_similarity import SeqPairSimilarity


class TestUtils(unittest.TestCase):
    seq_pair_sim = None
    subs_matrix = None

    def setUp(self):
        self.subs_matrix = get_grantham_subs_matrix()
        self.seq_pair_sim = SeqPairSimilarity(
            sequence1="LASIDPTFKAN",
            sequence2="ERQKNGGKSDSDDDEPAAKKKVEYPIAAAPPMMMP",
            substitution_matrix=self.subs_matrix,
            k=5
        )

    def test_get_length_difference(self):
        ld = SeqPairSimilarity.get_length_difference(4, 12)
        self.assertIsInstance(ld, float)

    def test_compute_kmer_maps(self):
        self.seq_pair_sim.compute_kmer_maps()
        self.assertIsNotNone(self.seq_pair_sim.kmer_count_map_1)
        self.assertIsInstance(self.seq_pair_sim.kmer_count_map_1, dict)

        self.assertIsNotNone(self.seq_pair_sim.kmer_count_map_2)
        self.assertIsInstance(self.seq_pair_sim.kmer_count_map_2, dict)

        for kmer_count in [self.seq_pair_sim.kmer_count_map_1, self.seq_pair_sim.kmer_count_map_2]:
            for kmer, count in kmer_count.items():
                self.assertIsInstance(kmer, str)
                self.assertEqual(5, len(kmer))
                self.assertIsInstance(count, int)
                self.assertGreater(count, 0)

    def test_generate_kmer_map(self):
        test_seq = "ERQKNGGKSDSDDDEPAAKKKVEYPIAAAPPMMMP"
        kmer_count_map = SeqPairSimilarity.generate_kmer_map(
            sequence=test_seq,
            k_value=6
        )
        self.assertIsInstance(kmer_count_map, dict)
        for k, v in kmer_count_map.items():
            self.assertIsInstance(k, str)
            self.assertEqual(6, len(k))
            self.assertIn(k, test_seq)
            self.assertIsInstance(v, int)
            self.assertGreater(v, 0)

    def test_get_kmer_similarity_score__error(self):
        with self.assertRaises(Exception) as e:
            SeqPairSimilarity.get_kmer_similarity_score(
                kmer1='ERQKNG',
                kmer2='TFKAN',
                substitution_matrix=self.subs_matrix
            )
        self.assertIn('K-Mer lengths', str(e.exception))

    def test_get_kmer_similarity_score(self):
        score = self.seq_pair_sim.get_kmer_similarity_score('LASID', 'DEPAA', self.seq_pair_sim.substitution_matrix_obj)
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 1)

    def test_generate_similarity_matrix(self):
        self.seq_pair_sim.compute_kmer_maps()
        self.seq_pair_sim.generate_similarity_matrix()
        self.assertIsNotNone(self.seq_pair_sim.similarity_matrix)
        self.assertIsInstance(self.seq_pair_sim.similarity_matrix, dict)
        for kmer, kmer_score in self.seq_pair_sim.similarity_matrix.items():
            self.assertIsInstance(kmer, str)
            self.assertLessEqual(len(kmer), 5)
            for kmer_in, score in kmer_score.items():
                self.assertIsInstance(kmer, str)
                self.assertLessEqual(len(kmer), 5)
                self.assertIsInstance(score, float)
                self.assertGreaterEqual(score, 0)
                self.assertLessEqual(score, 1)


if __name__ == '__main__':
    unittest.main()
