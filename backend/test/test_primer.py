import unittest

from backend.functions.primer import salt_correction, check_gc_clamp

SEQUENCE = 'atcgtagtcgcacgcgacgagtcg'
FRAG_LENGTH = 22


class PrimerTest(unittest.TestCase):
    def test_salt_correction(self):
        err_method = 3
        with self.assertRaises(ValueError):
            salt_correction(method=err_method, Na=0.0)

    def test_check_cg_clamp(self):
        not_clamp_seq = 'aaaaaaaaaaaaaaaaaaaaa'
        self.assertEqual(check_gc_clamp(not_clamp_seq), False)
        clamp_seq = 'aatcagcacgatgggg'
        self.assertEqual(check_gc_clamp(clamp_seq), True)
