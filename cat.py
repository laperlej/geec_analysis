import sys, argparse
from geec_analysis_lib.metadata import Metadata

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('input', nargs='+', help='The raw metadate file: metadata.json')
    args = parser.parse_args(sys.argv[1:])

    inputs = args.input

    metadatas = [Metadata.parse_metadatafile(input_json) for input_json in inputs]
    metadata = reduce(lambda x, y: x+y, metadatas)

    print str(metadata)

if __name__ == "__main__":
    main()
