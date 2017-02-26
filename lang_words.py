import argparse
import grammar

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')

    args = parser.parse_args()

    grammar.save_words(grammar.from_xml(args.input), args.output)
