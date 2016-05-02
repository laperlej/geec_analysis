import sys

class Matrix(object):
    def __init__(self, path):
        self.__load_matrix()

class Labels(object):
    def __init__(self, path):
        pass

def main():
    if len(sys.argv) < 3:
        print "Usage: python ari.py matrix_path labels_path"
        exit(1)

    matrix_path = sys.argv[1]
    labels_path = sys.argv[2]

if __name__ == "__main__":
    main()
