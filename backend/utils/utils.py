import logging
import pandas as pd
import re

logger = logging.getLogger(__name__)


def refiner(df: pd.DataFrame, conditions: str, pending=True):
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
