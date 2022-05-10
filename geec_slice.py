from __future__ import print_function
import sys, argparse, re
import traceback
import geec_analysis_lib.matrix as mtx
from geec_analysis_lib.annotate_tsv import *
import geec_analysis_lib.slice_matrix as sm
from geec_analysis_lib.labels import letter_label_to_int_label, int_label_to_letter_label

NAMES_REGEX = '[A-Z]+(-[A-Z]+)?(\\,[ ]?[A-Z]+(-[A-Z]+)?)*'
CLUSTER_REGEX = 'cluster\\([0-9]+\\)'

def load_matrix(matrix_file):
    """
    matrix geec_matrix filename
    return GeecMatrix
    """
    return mtx.Matrix.parse_matrixfile(matrix_file)

def parse_cluster_names(raw_names):
    """
    names raw list of names
    return list of cluster names
    raise Exception
    """
    names_str = ' '.join(raw_names)

    if not re.match(NAMES_REGEX, names_str):
        raise Exception('Bad format for the clusters groups. Must be something like that: A-C, E')

    names_subgroups = [sbg.strip() for sbg in names_str.split(',')]

    result = []
    for subgroup in names_subgroups:
        result.extend(convert_relative_clusters_to_explicit_list(subgroup))

    if len(result) != len(set(result)):
        raise Exception('Some clusters groups are prensent multiple times')

    return result

def convert_relative_clusters_to_explicit_list(subcluster):
    indvidual_letters = subcluster.split('-')

    if len(indvidual_letters) == 1:
        return indvidual_letters
    elif len(indvidual_letters) == 2:
        return make_letter_range(*indvidual_letters)
    else:
        raise Exception('Bad format for the clusters groups catched too late')

def make_letter_range(first_s, second_s):
    first = letter_label_to_int_label(first_s)
    second = letter_label_to_int_label(second_s)

    if second <= first:
        raise Exception('Bad letters range: ' + first_s + '-' + second_s)

    return [int_label_to_letter_label(x) for x in xrange(first, second + 1)]

def extract_wanted_file_names(annotate_tsv, names):
    cluster_header = find_cluster_header(annotate_tsv)
    row_indexes = annotate_tsv.make_filter(cluster_header, lambda x: x in names)
    return annotate_tsv.list_items('file_name', row_indexes)

def find_cluster_header(annotate_tsv):
    regex = re.compile(CLUSTER_REGEX)

    for header in annotate_tsv.list_headers():
        matched = regex.match(header)

        if matched:
            return header

    raise Exception('The annotate tsv file contains no cluster')

def main(argv):

    parser = argparse.ArgumentParser()
    parser.add_argument('matrix', help='The input matrix tsv file.')
    parser.add_argument('annotate_tsv', help='The input annotate tsv file.')
    parser.add_argument('clustersnames', nargs='*', help='The clusters names (e.g. A-E,H).')
    args = parser.parse_args(argv[1:])

    try:
        matrix = load_matrix(args.matrix)
        annotate_tsv = AnnotateTsv.load_annotate_tsv(args.annotate_tsv)
        names = parse_cluster_names(args.clustersnames)
        wanted_file_names = extract_wanted_file_names(annotate_tsv, names)

        print(sm.SliceMatrix.slice(matrix, wanted_file_names), end='')
    except IOError:
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    main(sys.argv)
