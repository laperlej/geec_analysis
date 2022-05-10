import sys, argparse
import traceback
from geec_analysis_lib.ari_builder import AriBuilder
import logging
from geec_analysis_lib.exception.geecanalysiserror import GeecAnalysisError
from geec_analysis_lib.exception.geecanalysisexception import GeecAnalysisException

logging.basicConfig()
logger = logging.getLogger(__name__)

def main(argv):

    parser = argparse.ArgumentParser()

    parser.add_argument('matrix', help='The input matrix tsv file.', type=str)
    parser.add_argument('metadata', help='The input metadata json file.', type=str)
    parser.add_argument(
        '--linkage',
        help='The linkage method. By default: "average" Options: "average", "complete", "weighted" or "single".',
        default='average',
        choices=['average', 'complete', 'weighted', 'single'],
        type=str)
    parser.add_argument(
        '--title',
        help='The title of the report.',
        default='epiGeEC Ari 1.0.0',
        type=str)
    parser.add_argument(
        '-b',
        nargs='*',
        help='The breakdown categories. If not specified, it will use all categories in metadata.',
        default=[],
        metavar='category',
        type=str)
    parser.add_argument(
        '-r',
        nargs='*',
        help='The annotation categories restrictions. If not specified, it will use all categories in metadata.',
        default=[],
        metavar='category',
        type=str)
    parser.add_argument(
        '-i',
        help='ignore User',
        action='store_true')
    args = parser.parse_args(argv[1:])

    ab = AriBuilder()
    ab.set_matrix_filename(args.matrix)
    ab.set_metadata_filename(args.metadata)
    ab.set_linkage_method(args.linkage)
    ab.set_breakdown_categories(args.b)
    ab.set_restriction_categories(args.r)
    ab.set_title(args.title)
    ab.set_ignore_user(args.i)

    try:
        a = ab.build()
        print a.run()
    except GeecAnalysisError as e:
        logger.error(e)
    except GeecAnalysisException as e:
        logger.critical(e, exc_info=e)
    except Exception as e:
        logger.exception(e)

if __name__ == "__main__":
    main(sys.argv)
