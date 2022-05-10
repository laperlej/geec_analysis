from __future__ import print_function
import sys, argparse
import traceback
import geec_analysis_lib.matrix as mtx
import geec_analysis_lib.slice_matrix as sm

def load_matrix(matrix_file):
    """
    matrix geec_matrix filename
    return GeecMatrix
    """
    return mtx.Matrix.parse_matrixfile(matrix_file)

def geec_slice_file_name(matrix_filename, file_names, output=None):
    matrix = load_matrix(matrix_filename)
    newmatrix = sm.SliceMatrix.slice(matrix, file_names)

    if output:
        with open(output, 'w') as output:
            output.write(str(newmatrix))
    else:
        print(newmatrix, end='')

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('matrix', help='The input matrix tsv file.')
    parser.add_argument('file_names', help='The input file_names text file.')
    args = parser.parse_args(argv[1:])

    with open(args.file_names, 'r') as f:
        filenames = f.read().split('\n')
    
    geec_slice_file_name(args.matrix, filenames)

if __name__ == "__main__":
    main(sys.argv)
