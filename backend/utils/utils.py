import logging
import re

logger = logging.getLogger(__name__)


def remove_unnecessary(seq):
    # type seq->string
    seq = str(seq)
    code_regex = re.compile(r'[0-9bd-fh-su-zBD-FH-SU-Z!-/:-@-`{-~]')
    detect = re.search(code_regex, seq)
    if detect:
        logger.error(f'action=remove_unnecessary error=NucBaseUnnecessaryError')
    removed_seq = re.sub(code_regex, '', seq).replace(' ', '').replace('\n', '').replace('\r', '')
    return removed_seq


def newline(seq, per=100):
    if len(seq) > per:
        broke_seq = ''
        for i in range(0, len(seq), per):
            broke_seq += seq[i: i+per] + '\n'
        return broke_seq
    return seq
