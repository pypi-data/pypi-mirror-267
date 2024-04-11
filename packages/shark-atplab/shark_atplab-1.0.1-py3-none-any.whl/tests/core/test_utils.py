import unittest
import os
from pathlib import Path

from shark_atplab import settings
from shark_atplab.core.utils import get_grantham_subs_matrix, read_fasta_file, form_sequence_pairs

FASTA_STR = """
>A0A5D0NPI2_9ACTN/46-124/PF14408
ISPPDWHRVELDPRTQIARYLDGDGQVIEAGKHGTKTTPPPTTTPIEPPARTGRWAGAGDHQLGGRHRRHGDRRAQSQR
>A0A646KIX7_STRJU/31-99/PF14408
TLGKPTGRVVGLDPETQTTIYEDAAGRRLEMGKHSTHRGVETDTTTNPGDGAGPDAMDEDADQRSEQDE
>A0A6B2U4B8_9ACTN/38-98/PF14408
VEDVPAGLDPTTQRGLYQLPNGTIVMSPGKHSRSRQGTEKSTKTGNRGDGSKARPDTDHSQ
>D7B9H0_NOCDD/63-116/PF14408
EVAAAVDRYVYDPVTQRGIDRLTGAPAVGKRSSGTKETTGEPDSARPSTEETTT
>E4N896_KITSK/19-87/PF14408
TTTVPQYTPVIDPETQIAVIVDEHGRTVELGSHGTSTSGLTPTTTTPGDGAGPGGATDSDSTESYDQDQ
>L1L3U6_9ACTN/21-80/PF14408
VGPPSYRAVTLDASTQTARYTGAAGQVMEMGKHGTSKTTGTASVSGGGDVQNPQPQTQDD
>A0A010RRY4_9PEZI/31-798/PF11489
PKIPPRPIKRFDRSVSPNPDRYAPSPLNESPFSKSPKATRSSPSNGFLSSHDPIHHRPGSVSMPSVGEEGNEYDAINDGFVKPPPKAPSSPEHTRFAAEDLKLHAPKPTVPAQSAKQRVMAVTRTDSDKAASYGIGKPSSDDTRPSSLRKKASSSALSQKSESAFGDEEHGIPEIGQRVPMNPNLGDVQAPSPAPGSGAAPESLRSGTPRNHSRKHSSRGFNELPPGSYGLHGHSSALPTDKFEKAWYDKHPDFLKKDCKPSLHDRQNDYAMSSTDLNKIVKETHSRGSGMGTSSSYVGTPSEEVGYQASAEYTSRISSPELQRIKSPQSPSKDSHPQVSVSSPDNATGSDDGTVHVDESHNRRRSFVSHDPGHENKYNAPILAEDESGDVHPYDLQPAVEPPPERSGSAFEIEKPNRPTSRPTSIYNNNQSQTDLVHTPLEDVEEYEPLFDEERPEAKKTEAEAASSKPRHKFPSKDVWEDAPDSVNYTAEVSTPEPTESERPSSRRRSELPTENPALEFARRQEELAEQEGRGVDAKQMKPVPAALQKTKEEARPAMSNRFPSRDVWEDTPESALHEAIVDTPEPKDESPVEKPFVPARPQKKGSQSSATAEPPSIPERPRKQNSTSEDKAKPAVSEKSKPQIPARPTKTLTSGVDSKEQDSAPKQKPAIPGKPAGGKIAALQAGFLSDLNKRLQLGPTAPKKEEPPAADVAEEKEKAPLSDARKGRARGPQRRAPAAKSPAPAAVEAKSGPTLSFSPLRICWSIG
>A0A084GGL0_PSEDA/1-436/PF11489
MSDNTDLRMSSAELNEIVHNTATRGASNFLGTPS
"""
FASTA_FILE_PATH = Path(settings.DATA_DIR) / 'test_sequences.fasta'


class TestUtils(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fasta_file = open(file=FASTA_FILE_PATH, mode='w')
        fasta_file.write(FASTA_STR)
        fasta_file.close()

    @classmethod
    def tearDownClass(cls):
        FASTA_FILE_PATH.unlink()

    def test_get_grantham_subs_matrix(self):
        sub_matrix_obj = get_grantham_subs_matrix()
        self.assertIsInstance(sub_matrix_obj, tuple)
        self.assertEqual(3, len(sub_matrix_obj))
        self.assertIsInstance(sub_matrix_obj[0], dict)
        self.assertIn(type(sub_matrix_obj[1]), [int, float])
        self.assertIn(type(sub_matrix_obj[2]), [int, float])

        for k1, v1 in sub_matrix_obj[0].items():
            self.assertIsInstance(k1, str)
            self.assertIsInstance(v1, dict)
            for k2, v2 in v1.items():
                self.assertIsInstance(k2, str)
                self.assertIn(type(v2), [int, float])

    def test_read_fasta_file(self):
        id_seq_map = read_fasta_file(file_path=FASTA_FILE_PATH)
        self.assertIsInstance(id_seq_map, dict)
        self.assertEqual(len(id_seq_map), 8)

        for k, v in id_seq_map.items():
            self.assertIsInstance(k, str)
            self.assertIsInstance(v, str)

    def test_form_sequence_pairs(self):
        id_seq_map = read_fasta_file(file_path=FASTA_FILE_PATH)
        seq_pairs = form_sequence_pairs(id_seq_map)
        self.assertEqual(len(seq_pairs), 36)

    def test_form_sequence_pairs_2lists(self):
        id_seq_map = read_fasta_file(file_path=FASTA_FILE_PATH)
        id_seq_map1 = dict(list(id_seq_map.items())[:2])
        id_seq_map2 = dict(list(id_seq_map.items())[2:5])
        seq_pairs = form_sequence_pairs(id_seq_map1, id_seq_map2)
        self.assertEqual(len(seq_pairs), 6)


if __name__ == '__main__':
    unittest.main()
