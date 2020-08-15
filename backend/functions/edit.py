import logging

from Bio import BiopythonWarning
from Bio.Alphabet import IUPAC
from Bio.Seq import Seq

from backend.utils.utils import newline, remove_unnecessary

logger = logging.getLogger(__name__)


class Editor(object):
    def __init__(self, input_seq):
        if type(input_seq) is not str:
            raise ValueError
        self._seq = remove_unnecessary(input_seq)

    def convert(self, mode='Reverse Complement'):
        if mode == 'Reverse Complement':
            seq_c = str(Seq(self._seq).reverse_complement())
            return newline(seq_c, 100)
        elif mode == 'Transcription':
            dna = Seq(self._seq, IUPAC.unambiguous_dna)
            m_rna = str(dna.transcribe())
            return newline(m_rna, 100)
        elif mode == 'Translation':
            dna = Seq(self._seq, IUPAC.unambiguous_dna)
            try:
                poly_amino = str(dna.translate(to_stop=True))
            except BiopythonWarning as e:
                logger.error(f'action=convert error={e}')
                raise
            return newline(poly_amino, 100)
        else:
            from backend.utils.log import custom_logger
            custom_logger.error({'action': 'convert', 'status': 'failed', 'error': ValueError.__name__})
            raise ValueError
