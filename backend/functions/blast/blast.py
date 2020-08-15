import logging
import multiprocessing
import os
import subprocess

from Bio.Blast.Applications import NcbiblastnCommandline, NcbimakeblastdbCommandline

from backend.utils.utils import remove_unnecessary

core = multiprocessing.cpu_count()
current_dir = os.path.dirname(__file__)
db_file_path = os.path.join(current_dir, 'Database')
ref_path = os.path.join(current_dir, 'blastsets')
query_path = os.path.join(current_dir, 'blast.fasta')

logger = logging.Logger(__name__)


def create_db(db_name: str) -> bool:
    blastsets = {
        'TAIR10_Whole_Genome': 'TAIR10_bac_con_20101028',
        'TAIR10_CDS': 'TAIR10_cds_20101214_updated',
        'TAIR10_Genes': 'TAIR10_cdna_20110103_representative_gene_model_updated'
    }
    # create Database directory
    if not os.path.isdir(db_file_path):
        os.makedirs(db_file_path)
        logger.info('Now, Database dir has been created!')
    # create blastsets directory
    if not os.path.isdir(ref_path):
        os.makedirs(ref_path)
        logger.info('Now, blastsets dir has been created!')
    if db_name not in blastsets.keys():
        logger.error('Entered a database that is not registered.')
        raise ValueError
    source = blastsets[db_name]
    source_path = os.path.join(ref_path, source)
    if not os.path.exists(source_path):
        subprocess.run(['curl', '-O',
                        'ftp://ftp.arabidopsis.org/home/tair/Sequences/blast_datasets/TAIR10_blastsets/' + source],
                       cwd=ref_path)
        logger.info('The source download is finished.')
    cline = NcbimakeblastdbCommandline(input_file=source_path, dbtype='nucl',
                                       parse_seqids=True, out=os.path.join(db_file_path, db_name))
    stdout, stderr = cline()
    if stderr:
        logger.debug(stderr)
        return False
    logger.debug(stdout)
    return True


def blastn(input_seq: str, db='TAIR10_Whole_Genome', word_size=11, gap_open=5, gap_extend=2, reward=2, penalty=-3,
           num_threads=core) -> str:
    if not check_usable():
        return 'Cannot be used'
    if not os.path.exists(os.path.join(db_file_path, db + '.nin')) or \
            not os.path.exists(os.path.join(db_file_path, db + '.nhr')):
        is_created = create_db(db_name=db)
        if not is_created:
            from backend.utils.log import custom_logger
            custom_logger.error({
                'action': 'create_db',
                'status': 'failed'
            })
            raise
    removed_seq = remove_unnecessary(input_seq)
    write_fasta(removed_seq)
    db_path = os.path.join(db_file_path, db)
    blast_result = NcbiblastnCommandline(db=db_path, query=query_path, word_size=word_size, gapopen=gap_open,
                                         gapextend=gap_extend, reward=reward, penalty=penalty,
                                         num_threads=num_threads)()[0]
    return blast_result


def write_fasta(seq):
    format_list = ['>user-submitted', seq]
    try:
        with open(query_path, mode='w') as f:
            f.write('\n'.join(format_list))
    except Exception as e:
        from backend.utils.log import custom_logger
        custom_logger.error({'action': 'write_fasta', 'error': f'{e}'})
        raise


def get_homology_count(query_seq_list, db='TAIR10_Whole_Genome', word_size=11, gap_open=5, gape_extend=2,
                       reward=2, penalty=-3, num_threads=core) -> list:
    if not check_usable():
        return ['Cannot be used'] * len(query_seq_list)
    if not os.path.exists(os.path.join(db_file_path, db + '.nin')) or \
            not os.path.exists(os.path.join(db_file_path, db + '.nhr')):
        is_created = create_db(db_name=db)
        if not is_created:
            from backend.utils.log import custom_logger
            custom_logger.error({
                'action': 'create_db',
                'status': 'failed'
            })
            raise
    db_path = os.path.join(db_file_path, db)
    homology_list = []
    for query_seq in query_seq_list:
        write_fasta(query_seq)
        out = NcbiblastnCommandline(db=db_path, query=query_path, word_size=word_size, gapopen=gap_open,
                                    gapextend=gape_extend, reward=reward, penalty=penalty, outfmt=6,
                                    num_threads=num_threads)()[0]

        number_of_homology = len(out.splitlines())
        homology_list.append(number_of_homology)
    return homology_list


def check_usable():
    status_code = subprocess.check_call(('blastn', '-help'), stdout=subprocess.DEVNULL)
    if status_code != 0:
        logging.error('You do not install blast+. You have to install to use this function.')
        return False
    return True
