import unittest

from backend.functions.edit import Editor


class SequenceTest(unittest.TestCase):
    def test_convert_reverse_complement(self):
        seq = 'ACTAGCTAGCTACGACA'
        e = Editor(seq)
        self.assertEqual(e.convert(mode='Reverse Complement'),
                         'TGTCGTAGCTAGCTAGT')

    def test_convert_transcription(self):
        seq = 'ACTAGCTAGCTACGACA'
        e = Editor(seq)
        self.assertEqual(e.convert(mode='Transcription'),
                         'ACUAGCUAGCUACGACA')

    def test_convert_translation(self):
        seq = 'ACTAGCTAGCTACGA'
        e = Editor(seq)
        self.assertEqual(e.convert(mode='Translation'),
                         'TS')
