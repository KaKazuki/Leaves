import logging

from flask import Blueprint, jsonify, request

from backend.functions.alignment.pairwise import needle, water, parse, prettier
from backend.functions.blast.blast import blastn, get_homology_count, check_usable
from backend.functions.edit import Editor
from backend.functions.primer import OligoCalculator
from backend.utils.utils import refiner

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
        return jsonify({'API': 'Alignment', 'message': 'not included value in Algorithm'}), 400
    if not enter_type:
        return jsonify({'API': 'Alignment', 'message': 'not include value in EnterType'}), 400
    if not str_per_line:
        per_line = 100
    else:
        per_line = int(str_per_line)
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
    # calculate -> result
    str_cut_length = request_json['frag_length']
    input_seq = request_json['input_seq']
    cg_clamp = request_json['cg_clamp']
    self_comp = request_json['self_comp']
    if not str_cut_length:
        return jsonify({'API': 'Primer', 'message': 'not included value in frag_length'}), 400
    if not input_seq:
        return jsonify({'API': 'Primer', 'message': 'not contain value in input_seq'}), 400
    cut_length = int(str_cut_length)
    oligo_calculator = OligoCalculator(input_seq, cut_length)
    result_df = oligo_calculator.get_result(selfcomp=self_comp, gc_clamp=cg_clamp)
    # narrow down
    refined_df, pending_conditions = refiner(result_df, conditions=request_json['conditions'])
    # add column as number of homology
    num_of_homology_list = get_homology_count(refined_df['fragment'])
    refined_df['homology'] = num_of_homology_list
    # narrow down by number of homology
    if pending_conditions:
        refined_df, _ = refiner(refined_df, conditions=pending_conditions, pending=False)
    # sorted by tm_value
    refined_df_sorted = refined_df.sort_values('breslauer', ascending=False)
    logging.info({'API': 'Primer', 'status': 'finished'})
    return refined_df_sorted.to_json(orient='records')
