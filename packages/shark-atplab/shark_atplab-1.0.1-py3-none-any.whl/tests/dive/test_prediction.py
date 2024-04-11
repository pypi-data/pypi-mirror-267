import unittest

from shark_atplab.dive.prediction import Prediction

test_sequence1 = 'SSSSPINTHGVSTTVPSSNNTIIPSSDGVSLSQTDYFDTVHNRQSPSRRESPVTVFRQPSLSHSKSLHKDSKNKVPQISTNQSHPSAVSTANTPGPSPN'
test_sequence2 = 'LIDDKRRMEIGPSSGRLPPFSNVHSLQTSANPTQIKGVNDISHWSQEFQGSNSIQNRNADTGNSEKAWQRGSTTASSRFQYPNTM'
test_sequence3 = 'VAEREFNGRSNSLHANFTSPVPRTVLDHHRHELTFCNPNNTTGFKTITPSPPTQHQSILPTAVDNVPRSKSVSSLPVSGFPPLIVKQQQQQQLNSSSSASALPSIHSPLTNEH'

id_seq_map1 = {
    'A0A5D0NPI2_9ACTN/46-124/PF14408': 'ISPPDWHRVELDPRTQIARYLDGDGQVIEAGKHGTKTTPPPTTTPIEPPARTGRWAGAGDHQLGGRHRRHGDRRAQSQR',
    'A0A646KIX7_STRJU/31-99/PF14408': 'TLGKPTGRVVGLDPETQTTIYEDAAGRRLEMGKHSTHRGVETDTTTNPGDGAGPDAMDEDADQRSEQDE',
    'A0A6B2U4B8_9ACTN/38-98/PF14408': 'VEDVPAGLDPTTQRGLYQLPNGTIVMSPGKHSRSRQGTEKSTKTGNRGDGSKARPDTDHSQ'
}

id_seq_map2 = {
    'D7B9H0_NOCDD/63-116/PF14408': 'EVAAAVDRYVYDPVTQRGIDRLTGAPAVGKRSSGTKETTGEPDSARPSTEETTT',
    'E4N896_KITSK/19-87/PF14408': 'TTTVPQYTPVIDPETQIAVIVDEHGRTVELGSHGTSTSGLTPTTTTPGDGAGPGGATDSDSTESYDQDQ'
}


class TestPrediction(unittest.TestCase):
    def test_predict(self):
        pred = Prediction(q_sequence_id_map=id_seq_map1, t_sequence_id_map=id_seq_map2)

        self.assertIsInstance(pred.unique_sequence_pairs, list)
        self.assertIsNotNone(pred.unique_sequence_pairs)
        self.assertEqual(6, len(pred.unique_sequence_pairs))
        for pair in pred.unique_sequence_pairs:
            self.assertIsInstance(pair, dict)
            for k in ['seq_id1', 'seq_id2', 'sequence1', 'sequence2']:
                self.assertIn(k, pair)

        output = pred.predict()
        self.assertIsInstance(output, list)
        self.assertEqual(6, len(output))
        for i in range(6):
            self.assertIsInstance(output[i], dict)
            for k in ['seq_id1', 'sequence1', 'seq_id2', 'sequence2', 'similarity_scores_k', 'pred_proba']:
                self.assertIn(k, list(output[i].keys()))

            self.assertIsInstance(output[i]['similarity_scores_k'], list)
            self.assertEqual(10, len(output[i]['similarity_scores_k']))
            self.assertGreaterEqual(output[i]['pred_proba'], 0)
            self.assertLessEqual(output[i]['pred_proba'], 1)

    def test_compute_input_vector(self):
        similarity_scores_k = Prediction.compute_input_vector(sequence1=test_sequence1, sequence2=test_sequence2)
        self.assertIsInstance(similarity_scores_k, list)
        self.assertEqual(len(similarity_scores_k), 10)
        for score in similarity_scores_k:
            self.assertIsInstance(score, float)
            self.assertGreaterEqual(score, 0)
            self.assertLessEqual(score, 1)


if __name__ == '__main__':
    unittest.main()
