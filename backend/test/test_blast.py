import unittest

from backend.functions.blast.blast import blastn, get_homology_count


class BlastTest(unittest.TestCase):
    def test_blastn_db(self):
        not_registered_db = 'test'
        input_seq = 'atcgatgatcgatcgacg'
        with self.assertRaises(ValueError):
            blastn(input_seq=input_seq, db=not_registered_db)

    def test_get_number_of_homology_db(self):
        not_registered_db = 'test'
        query_seq_list = ['tactagcatcgatagagca']
        with self.assertRaises(ValueError):
            get_homology_count(query_seq_list=query_seq_list, db=not_registered_db)