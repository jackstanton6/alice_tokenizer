import argparse
import sys

from .terminal import terminal
from ..tokenisation import Tokeniser

"""
def train(
        data: str,
        vocab_size: int, 
        chunks: int, 
        name: str, 
        save_format: str, 
        save_to_file: bool, 
        pretokenize: bool, 
        do_tests: bool,
        quiet: bool
    ) -> dict:
"""

def main():

    parser = argparse.ArgumentParser(description="the alice tokenizer CLI app for tokenising and training.")

    parser.add_argument("--train", action="store_true", help="activate training mode")

    parser.add_argument("--data_file", "-d", type=str, default = None, help="the datafile name containing your text data.")
    parser.add_argument("--vocab_size", "-v", type=int, default = 32_000, help="target vocab size")
    parser.add_argument("--chunks", "-c", type=int, default = 4_000, help="number of chunks to split training data into, should be a factor of vocab size")
    parser.add_argument("--name", "-n", type=str, default = 'bob', help="name of the final tokenizer/vocab")
    parser.add_argument("--format", "-f", type=str, default = 'json', help="save format of the final vocab, dont change from json")
    parser.add_argument("--save_to_file", action="store_true", help="option on whether to save the vocab file to the disk")
    parser.add_argument("--pretokenize", "--pretokenise", "-p", action="store_true", help="option on whether to pretokenise the training data")
    parser.add_argument("--do_tests", action="store_true", help="option on whether to run tests after training")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        terminal()
    else:
        tok = Tokeniser(build=True)
        if args.data_file is None:
            raise ValueError("Data file must be declared!")
        tok.set_data(args.data_file)
        tok.train(
            vocab_size=args.vocab_size,
            chunks=args.chunks,
            name=args.name,
            save_format=args.format,
            save_to_file=args.save_to_file,
            pretokenize=args.pretokenize,
            do_tests=args.do_tests,
            quiet=False
        )
        terminal(tokenizer=tok)
