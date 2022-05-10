import sys, argparse
import traceback
import geec_analysis_lib.annotate_builder as annotate_builder
import geec_analysis_lib.string_builder as sb
import logging
from geec_analysis_lib.exception.geecanalysiserror import GeecAnalysisError
from geec_analysis_lib.exception.geecanalysisexception import GeecAnalysisException

sys.setrecursionlimit(10000)
logging.basicConfig()
logger = logging.getLogger(__name__)

class RangeType(object):
    def __init__(self, minv, maxv):
        self.minv = minv
        self.maxv = maxv

    def __call__(self, x):
        value = int_type(x)

        if value < self.minv or value > self.maxv:
            raise argparse.ArgumentTypeError('The value "{}" is not between {:,} and {:,}.'.format(value, self.minv, self.maxv))

        return value

def int_type(x):
    try:
        return int(x)
    except ValueError:
        raise argparse.ArgumentTypeError('{!r} is not an integer.'.format(x))

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('matrix', help='The input matrix tsv file.', type=str)
    parser.add_argument('--rmat', help='Write a reordered matrix.', type=str)
    parser.add_argument('--pdf', help='The output pdf file.', type=str)
    parser.add_argument('--tsv', help='The output tsv file.', type=str)
    parser.add_argument(
        '--title',
        help='The title of the report.',
        default='epiGeEC Annotate Matrix, k=%(nb_clusters) clusters',
        type=str)
    parser.add_argument(
        '--mds',
        help='Add a Multidimensional scaling figure (MDS) inside the pdf file.',
        action='store_true')
    parser.add_argument(
        '--seed',
        help='The seed number to generate the MDS [0-4294967295].',
        type=RangeType(0, 4294967295))
    parser.add_argument('metadata', help='The input metadata json file.', type=str)
    parser.add_argument(
        '-k',
        help='The numbers of clusters [1-4294967295]. If not specified, an optimal clustering is used.',
        type=RangeType(1, 4294967295))
    parser.add_argument(
        '--linkage',
        help='The linkage method. By default: "average" Options: "average", "complete", "weighted" or "single".',
        default='average',
        choices=['average', 'complete', 'weighted', 'single'],
        type=str)
    parser.add_argument(
        'categories',
        nargs='*',
        help='The categories used inside the reports. If not specified, it will use all categories in metadata.',
        default=[],
        metavar='category',
        type=str)
    args = parser.parse_args(argv[1:])

    ab = annotate_builder.AnnotateBuilder()
    ab.set_reordered_matrix_filename(args.rmat)
    ab.set_matrix_filename(args.matrix)
    ab.set_metadata_filename(args.metadata)
    ab.set_desired_nb_clusters(args.k)
    ab.set_groups(args.categories)
    ab.set_pdf_file(args.pdf)
    ab.set_title(sb.StringBuilder(args.title))
    ab.set_tsv_file(args.tsv)
    ab.set_seed(args.seed)
    ab.set_mds(args.mds)
    ab.set_linkage_method(args.linkage)

    try:
        app = ab.build()
        app.run()
    except GeecAnalysisError as e:
        logger.error(e)
    except GeecAnalysisException as e:
        logger.critical(e, exc_info=e)
    except Exception as e:
        logger.exception(e)


if __name__ == "__main__":
    main(sys.argv)
