from io import StringIO

from Bio import SeqIO
from Bio import pairwise2
from Bio.SubsMat.MatrixInfo import blosum62

from backend.functions.alignment.matrix import dnafull


# global
def needle(seq1: str, seq2: str, enter_type, gap_penalty=-10, extend_penalty=-5):
    if enter_type == 'DNA':
        alignments = pairwise2.align.globalds(seq1.upper(), seq2.upper(), dnafull, gap_penalty, extend_penalty)
    elif enter_type == 'PROTEIN':
        alignments = pairwise2.align.globalds(seq1.upper(), seq2.upper(), blosum62, gap_penalty, extend_penalty)
    else:
        raise TypeError
    return alignments


# local
def water(seq1: str, seq2: str, enter_type, gap_penalty=-10, extend_penalty=-5):
    if enter_type == 'DNA':
        alignments = pairwise2.align.localds(seq1.upper(), seq2.upper(), dnafull, gap_penalty, extend_penalty)
    elif enter_type == 'PROTEIN':
        alignments = pairwise2.align.localds(seq1.upper(), seq2.upper(), blosum62, gap_penalty, extend_penalty)
    else:
        raise TypeError
    return alignments


def parse(data: str):
    for record in SeqIO.parse(StringIO(data), "fasta"):
        if hasattr(record, '__iter__'):
            return record.id, record.seq.upper()
        else:
            break
    name = None
    return name, data.upper()


def prettier(align1, align2, _, begin, end, name1, name2, algorithm_name, full_sequence=True, per_line=100) -> str:
    # _ is score
    if name1 is None:
        name1 = 'seq1'
    if name2 is None:
        name2 = 'seq2'

    align_begin = begin
    align_end = end
    start1 = ""
    start2 = ""
    start_m = begin
    if full_sequence:
        start_m = 0
        begin = 0
        end = len(align1)

    if isinstance(align1, list):
        align1 = [a + " " for a in align1]
        align2 = [a + " " for a in align2]

    s1_line = ["{:>{width}}".format(start1, width=start_m)]
    m_line = [" " * start_m]
    s2_line = ["{:>{width}}".format(start2, width=start_m)]

    for n, (a, b) in enumerate(zip(align1[begin: end], align2[begin: end])):
        m_len = max(len(a), len(b))
        s1_line.append("{:^{width}}".format(a, width=m_len))
        s2_line.append("{:^{width}}".format(b, width=m_len))
        if full_sequence and (n < align_begin or n >= align_end):
            m_line.append("{:^{width}}".format(" ", width=m_len))
            continue
        if a == b:
            m_line.append("{:^{width}}".format("|", width=m_len))
        elif a.strip() == "-" or b.strip() == "-":
            m_line.append("{:^{width}}".format("*", width=m_len))
        else:
            m_line.append("{:^{width}}".format(".", width=m_len))

    space_del_s1 = "".join(s1_line)
    space_del_m = "".join(m_line)
    space_del_s2 = "".join(s2_line)

    difference = abs(len(name2) - len(name1))
    required_space = " " * difference
    name_max = max(len(name1), len(name2))
    name_m = " " * name_max
    if len(name1) > len(name2):
        name2 = name2 + required_space
    elif len(name1) < len(name2):
        name1 = name1 + required_space
    else:
        pass
    name1 += " " * 3
    name2 += " " * 3
    name_m += " " * 3

    s1_100 = [name1 + space_del_s1[i: i + per_line] for i in range(0, len(space_del_s1), per_line)]
    m_100 = [name_m + space_del_m[i: i + per_line] for i in range(0, len(space_del_m), per_line)]
    s2_100 = [name2 + space_del_s2[i: i + per_line] for i in range(0, len(space_del_s2), per_line)]
    formed_result = ''
    for i in range(len(s1_100)):
        formed_result += "\n".join([s1_100[i], m_100[i], s2_100[i]]) + '\n' * 2
    formed_result += algorithm_name
    return formed_result
