import numpy as np
import pandas as pd
from Bio import Seq
from Bio.SeqUtils import GC

from backend.utils.utils import remove_unnecessary
from backend.functions.blast.blast import get_homology_count

# Breslauer et al. (1986), Proc Natl Acad Sci USA 83: 3746-3750
Breslauer = {
    "init": (0, 0),
    "AA": (-9.1, -24), "TT": (-9.1, -24), "AT": (-8.6, -23.9), "TA": (-6.0, -16.9),
    "CA": (-5.8, -12.9), "TG": (-5.8, -12.9), "GT": (-6.5, -17.3), "AC": (-6.5, -17.3),
    "CT": (-7.8, -20.8), "AG": (-7.8, -20.8), "GA": (-5.6, -13.5), "TC": (-5.6, -13.5),
    "CG": (-11.9, -27.8), "GC": (-11.1, -26.7), "GG": (-11.0, -26.6), "CC": (-11.0, -26.6)
}

# Allawi and SantaLucia (1997), Biochemistry 36: 10581-10594
SantaLucia = {
    'init': (0, 0), 'init_A/T': (2.3, 4.1), 'init_G/C': (0.1, -2.8),
    "init_oneG/C": (0, 0), "init_allA/T": (0, 0), "init_5T/A": (0, 0),
    'AA': (-7.9, -22.2), 'TT': (-7.9, -22.2), 'AT': (-7.2, -20.4), 'TA': (-7.2, -21.3),
    'CA': (-8.5, -22.7), 'TG': (-8.5, -22.7), 'GT': (-8.4, -22.4), 'AC': (-8.4, -22.4),
    'CT': (-7.8, -21.0), 'AG': (-7.8, -21.0), 'GA': (-8.2, -22.2), 'TC': (-8.2, -22.2),
    'CG': (-10.6, -27.2), 'GC': (-9.8, -24.4), 'GG': (-8.0, -19.9), 'CC': (-8.0, -19.9)
}


def narrow_down(df: pd.DataFrame, conditions: str, pending=True):
    if not conditions:
        return df, None
    if conditions[-1] == ';':
        conditions = conditions.rstrip(';')
    conditions_list = conditions.split(';')
    pending_conditions = ''
    result = []
    for condition in conditions_list:
        condition_list = condition.split()
        if len(condition_list) != 3:
            raise TypeError
        column = condition_list[0]
        if column == 'homology' and pending:
            pending_conditions += condition + ';'
            continue
        sign = condition_list[1]
        value = int(condition_list[2])
        if len(result) != 0:
            df = result[-1]
        if sign == '>=':
            conditional_df = df[df[column] >= value]
        elif sign == '<=':
            conditional_df = df[df[column] <= value]
        elif sign == '<':
            conditional_df = df[df[column] < value]
        elif sign == '>':
            conditional_df = df[df[column] > value]
        else:
            raise TypeError
        result.append(conditional_df)
    return result[-1], pending_conditions


# SantaLucia (1998), Proc Natl Acad Sci USA 95: 1460-1465
def salt_correction(method: int, Na: float, K=0.0, Tris=0, Mg=0.0, dNTPs=0.0, seq=None):
    mono = Na + K + Tris / 2.0
    if sum((K, Mg, Tris, dNTPs)) > 0 and dNTPs < Mg and method == 2:
        mono += 120 * np.sqrt(Mg - dNTPs)
    mono = mono * 1e-3
    if method == 1:
        corr = 16.6 * np.log10(mono)
        return corr
    elif method == 2:
        corr = 0.368 * (len(seq) - 1) * np.log(mono)
        return corr
    elif method == 3:
        corr = ((4.29 * GC(seq) / 100 - 3.95) * 1e-5 * np.log(mono)) + 9.40e-6 * np.log(mono) ** 2
        return corr
    else:
        raise ValueError


class NearestNeighbor(object):
    R = 1.987
    d_h = 0
    d_s = 1

    def __init__(self, seq, Na=50.0, mol=0.5):
        if type(seq) is not str or type(Na) is not float and type(mol) is not float:
            raise ValueError
        # to upper
        self.seq = seq.upper()
        # mM
        self.Na = Na
        # μM -> M
        self.mol = mol * 1e-6

    def breslauer(self) -> int:
        # set parameter table
        nn_table = Breslauer
        delta_h = nn_table['init'][self.d_h]
        delta_s = nn_table['init'][self.d_s]
        for base_number in range(len(self.seq) - 1):
            interaction = self.seq[base_number: base_number + 2].upper()
            delta_h += nn_table[interaction][self.d_h]
            delta_s += nn_table[interaction][self.d_s]
        denominator = 1000 * delta_h
        numerator = delta_s + (self.R * np.log(self.mol / 4)) - 10.8
        melting_temp = (denominator / numerator) - 273.15 + salt_correction(Na=self.Na, method=1)
        return round(melting_temp, 1)

    def santalucia(self) -> int:
        # set parameter table
        nn_table = SantaLucia
        delta_h = nn_table['init'][self.d_h]
        delta_s = nn_table['init'][self.d_s]
        if GC(self.seq) == 0:
            delta_h += nn_table["init_allA/T"][self.d_h]
            delta_s += nn_table["init_allA/T"][self.d_s]
        else:
            delta_h += nn_table["init_oneG/C"][self.d_h]
            delta_s += nn_table["init_oneG/C"][self.d_s]

        # Type: Penalty if 5' end is T
        if self.seq.startswith("T"):
            delta_h += nn_table["init_5T/A"][self.d_h]
            delta_s += nn_table["init_5T/A"][self.d_s]
        if self.seq.endswith("A"):
            delta_h += nn_table["init_5T/A"][self.d_h]
            delta_s += nn_table["init_5T/A"][self.d_s]

        # Type: Different values for G/C or A/T terminal basepairs
        ends = self.seq[0] + self.seq[-1]
        AT = ends.count('A') + ends.count('T')
        CG = ends.count('C') + ends.count('G')
        delta_h += nn_table["init_A/T"][self.d_h] * AT
        delta_s += nn_table["init_A/T"][self.d_s] * AT
        delta_h += nn_table["init_G/C"][self.d_h] * CG
        delta_s += nn_table["init_G/C"][self.d_s] * CG

        for base_number in range(len(self.seq) - 1):
            interaction = self.seq[base_number: base_number + 2]
            delta_h += nn_table[interaction][self.d_h]
            delta_s += nn_table[interaction][self.d_s]
        delta_s += salt_correction(seq=self.seq, Na=self.Na, method=2)
        melting_temp = (delta_h * 1000) / (delta_s + (self.R * np.log(self.mol / 4))) - 273.15
        return round(melting_temp, 1)


def get_fragments(seq: str, cut_length: int):
    # upper -> adjust to params_key
    if type(seq) != str or type(cut_length) != int:
        raise TypeError
    upper_seq = seq.upper()
    frag_list = []
    seq_length = len(upper_seq)
    pos_list = []
    if seq_length <= cut_length:
        frag_list.append(upper_seq)
        return frag_list, [[0, seq_length]]
    for base in range(seq_length - 1):
        frag = upper_seq[base: base + cut_length]
        if len(frag) != cut_length:
            break
        frag_list.append(frag)
        pos_list.append([base, base + cut_length])
    return frag_list, pos_list


def check_selfcomp(seq: str, threshold=4) -> bool:
    if type(seq) != str or type(threshold) != int:
        raise TypeError
    r_seq = seq[::-1]
    d = {}
    for i in range(threshold, len(seq) + 1):
        s = []
        for base in range(len(seq) - 1):
            r_oligo = r_seq[base: base + i]
            if len(r_oligo) != i:
                break
            r_c_seq = Seq.complement(r_oligo)
            if r_c_seq in seq:
                s.append(r_c_seq)
                d[i] = s
    if not d:
        return False
    max_key = max(d.keys())
    if max_key >= 5 or len(d[max_key]) >= 5:
        return True
    return False


def check_gc_clamp(seq, last=5, threshold=4) -> bool:
    three_dash_end = seq[-last:len(seq) + 1].upper()
    number_of_g = three_dash_end.count('G')
    number_of_c = three_dash_end.count('C')
    if number_of_c + number_of_g >= threshold:
        return True
    return False


def view_position(full_seq, pos_list, per_line=100):
    begin, end = 0, 1
    length = len(full_seq)
    marked_line = ' ' * pos_list[begin] + \
                  '>' * (pos_list[end] - pos_list[begin]) + \
                  ' ' * (length - pos_list[end])
    seq_line = full_seq.upper()
    seq_line_100 = [seq_line[i: i + per_line] for i in range(0, len(seq_line), per_line)]
    marked_line_100 = [marked_line[i: i + per_line] for i in range(0, len(marked_line), per_line)]

    marked_result = ''
    for i in range(len(seq_line_100)):
        marked_result += '\n'.join([marked_line_100[i], seq_line_100[i]]) + '\n'
    return marked_result


def calculate(sequence, cut_length, conditions, cg_clamp, self_comp) -> pd.DataFrame:
    sequence = remove_unnecessary(sequence).upper()
    frag_list, position_list = get_fragments(seq=sequence, cut_length=cut_length)
    used_frag_list = []
    rev_comp_list = []
    tm_list_breslauer = []
    tm_list_santalucia = []
    cg_list = []
    marked_list = []
    for frag, pos in zip(frag_list, position_list):
        if cg_clamp:
            if check_gc_clamp(frag, last=5):
                continue
        if self_comp:
            if check_selfcomp(frag, threshold=4):
                continue
        used_frag_list.append(frag)
        rev_comp_list.append(str(Seq.reverse_complement(frag)))
        nn = NearestNeighbor(frag)
        melting_temp_breslauer = nn.breslauer()
        melting_temp_santalucia = nn.santalucia()
        cg_content = round(GC(frag), 1)
        marked_result = view_position(full_seq=sequence, pos_list=pos)
        tm_list_breslauer.append(melting_temp_breslauer)
        tm_list_santalucia.append(melting_temp_santalucia)
        cg_list.append(cg_content)
        marked_list.append(marked_result)
    df = pd.DataFrame({
        'fragment': used_frag_list,
        'rev_comp': rev_comp_list,
        'breslauer': tm_list_breslauer,
        'santalucia': tm_list_santalucia,
        'cg_content': cg_list,
        'position': marked_list
    })
    # narrow down except homology
    filtered_df, homology_condition = narrow_down(df, conditions=conditions)
    homology_list = get_homology_count(filtered_df['fragment'])
    filtered_df['homology'] = homology_list
    # narrowed down by homology
    if homology_condition:
        filtered_df, _ = narrow_down(filtered_df, homology_condition, pending=False)
    # sorted by breslauer
    filtered_df_s = filtered_df.sort_values('breslauer', ascending=False)
    return filtered_df_s


if __name__ == '__main__':
    nn = NearestNeighbor('cgagcacgatgctagcagat')
    print(nn.santalucia())
    from Bio.SeqUtils import MeltingTemp
    print(MeltingTemp.Tm_NN('cgagcacgatgctagcagat'.upper(), Na=50, saltcorr=6, dnac1=250, dnac2=250))
