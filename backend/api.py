import logging

from flask import Blueprint, jsonify, request

from backend.functions.alignment.pairwise import needle, water, parse, prettier
from backend.functions.blast.blast import blastn, check_usable
from backend.functions.edit import Editor
from backend.functions.primer import calculate

logging.basicConfig(level=logging.INFO)
api = Blueprint('api', __name__)


@api.route('/alignment', methods=['POST'])
def pairwise_alignment():
    request_json = request.json
    required = ('SeqData1', 'SeqData2', 'EnterType', 'Algorithm')
    if not all(k in request_json for k in required):
        return jsonify({'API': 'Alignment', 'message': 'missing value'}), 400
    logging.info({'API': 'Alignment', 'status': 'start', 'request': request_json})
    seq_data_1 = request_json['SeqData1']
    seq_data_2 = request_json['SeqData2']
    enter_type = request_json['EnterType']
    algorithm = request_json['Algorithm']
    str_per_line = request_json['PerLine']
    if not seq_data_1:
        return jsonify({'API': 'Alignment', 'message': 'not included value in SeqData1'}), 400
    if not seq_data_2:
        return jsonify({'API': 'Alignment', 'message': 'not included value in SeqData2'}), 400
    if not algorithm:
        algorithm = 'Needleman-Wunsch (Global)'
    if not enter_type:
        enter_type = 'DNA'
    if not str_per_line:
        per_line = 100
    else:
        per_line = int(str_per_line)
        if not (100 < per_line <= 250):
            per_line = 100
    # parse
    name1, seq1 = parse(seq_data_1)
    name2, seq2 = parse(seq_data_2)
    # alignment
    if algorithm == 'Needleman-Wunsch (Global)':
        result = needle(seq1, seq2, enter_type)
        algorithm_name = 'Needleman-Wunsch'
    elif algorithm == 'Smith-Waterman (Local)':
        result = water(seq1, seq2, enter_type)
        algorithm_name = 'Smith-Waterman'
    else:
        raise ValueError
    # formed
    formed_result = prettier(*result[0], name1=name1, name2=name2, algorithm_name=algorithm_name, per_line=per_line)
    response = {
        'result': formed_result
    }
    logging.info({'API': 'Alignment', 'status': 'finished'})
    return response


@api.route('/blast', methods=['POST', 'GET'])
def blast():
    if request.method == 'POST':
        request_json = request.json
        logging.info({'API': 'Blast', 'status': 'start', 'request': request_json})
        input_seq = request_json['inputSeq']
        db = request_json['db']
        if not input_seq:
            return jsonify({'API': 'Blast', 'message': 'not included value in input_seq'})
        blast_result = blastn(input_seq=input_seq, db=db)
        response = {
            'result': blast_result
        }
        logging.info({'API': 'Blast', 'status': 'finished'})
        return response

    if request.method == 'GET':
        response = {
            'usable': check_usable()
        }
        return response


@api.route('/conversion', methods=['POST'])
def convert():
    request_json = request.json
    required = ('mode', 'input_seq')
    if not all(k in request_json for k in required):
        return jsonify({'API': 'Conversion', 'message': 'missing value'}), 400
    logging.info({'API': 'Edit', 'input_seq': request_json['input_seq'], 'mode': request_json['mode']})
    input_seq = request_json['input_seq']
    mode = request_json['mode']
    if not input_seq:
        return jsonify({'API': 'Conversion', 'message': 'not included value in input_seq'})
    if not mode:
        return jsonify({'API': 'Conversion', 'message': 'not included value in mode'})
    editor = Editor(input_seq)
    edited_seq = editor.convert(mode)
    result = {
        'result': edited_seq
    }
    return result


@api.route('/primer', methods=['POST'])
def primer():
    logging.info({'API': 'Primer', 'status': 'start', 'request': request.json})
    request_json = request.json
    # check
    required = ('input_seq', 'frag_length', 'conditions')
    if not all(k in request_json for k in required):
        return jsonify({'API': 'Primer', 'message': 'missing value'}), 400
    str_cut_length = request_json['frag_length']
    input_seq = request_json['input_seq']
    cg_clamp = request_json['cg_clamp']
    self_comp = request_json['self_comp']
    conditions = request_json['conditions']
    if not input_seq:
        return jsonify({'API': 'Primer', 'message': 'not contain value in input_seq'}), 400
    cut_length = int(str_cut_length)
    if not (18 < cut_length <= 40):
        cut_length = 22
    # only one side
    if not ('[' and ']' in input_seq):
        result_df = calculate(sequence=input_seq, cut_length=cut_length,
                              self_comp=self_comp, cg_clamp=cg_clamp, conditions=conditions)
        logging.info({'API': 'Primer', 'status': 'finished'})
        return result_df.to_json(orient='records')
    # both forward and reverse
    left = input_seq.split('[')[0]
    right = input_seq.split(']')[1]
    forward_df = calculate(sequence=left, cut_length=cut_length,
                           self_comp=self_comp, cg_clamp=cg_clamp, conditions=conditions)
    reverse_df = calculate(sequence=right, cut_length=cut_length,
                           self_comp=self_comp, cg_clamp=cg_clamp, conditions=conditions)
    logging.info({'API': 'Primer', 'status': 'finished'})
    result = {
        'forward': forward_df.to_dict(orient='records'),
        'reverse': reverse_df.to_dict(orient='records')
    }
    return result
