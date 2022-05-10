import sys, argparse
from geec_analysis_lib.metadata import Metadata
import traceback, json, re

def load_metadata(filenames):
    metadatas = [Metadata.parse_metadatafile(input_json) for input_json in filenames]
    return reduce(lambda x, y: x+y, metadatas)

def load_patterns(pattern, is_file):
    if is_file:
        with open(pattern, 'r') as text_file:
            return [line.strip() for line in text_file]
    else:
        return [pattern]

def grep(metadata, pattern, is_regex, is_file, is_inverted):
    patterns = load_patterns(pattern, is_file)

    if is_regex:
        return metadata.match(patterns, is_inverted)
    else:
        return metadata.find(patterns, is_inverted)

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-v', action='store_true', help='Invert the match. Like not the pattern.')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-e', action='store_true', help='The pattern is a regex for the research.')
    group.add_argument('-f', action='store_true', help='The patterns are in a file.')

    parser.add_argument('pattern', help='The pattern for the research.')
    parser.add_argument('inputs', nargs='+', help='The raw metadate file: metadata.json')
    args = parser.parse_args(sys.argv[1:])

    inputs_json = args.inputs
    pattern = args.pattern
    is_regex = args.e
    is_file = args.f
    is_inverted = args.v

    metadata = load_metadata(inputs_json)

    print str(grep(metadata, pattern, is_regex, is_file, is_inverted))

if __name__ == "__main__":
    main()
