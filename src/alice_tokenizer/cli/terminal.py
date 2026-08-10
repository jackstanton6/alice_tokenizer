import random
import sys

from ..util.logo import logo
from ..util.helpfile import helpfile
from ..tokenisation import Tokeniser
from ..train_tokeniser import test_phrases

def terminal(tokenizer: Tokeniser = Tokeniser()):
    print(logo)
    print(f"Using {tokenizer.name} tokenizer. {tokenizer.vocab_size} vocab size.")
    print("Use /? or /help to see commands.")
    while True:
        user_in = input("> ")
        if user_in in ['/exit', '/bye']:
            print("bye")
            sys.exit(1)
        elif user_in in ['/help', '/?']:
            print(helpfile)
        elif user_in == "/test":
            phrase = random.choice(test_phrases)
            print(phrase)
            tokenizer.visualise(phrase)
        else:
            split = user_in.split(" ", maxsplit=1)
            command = split[0]
            if command[0] != "/":
                print(tokenizer.tokenise(user_in))
                continue
            if len(split) < 2:
                print("no input provided to command.")
                continue
            phrase = user_in.split(" ", maxsplit=1)[1]
            if command in ['/v', '/visual']:
                tokenizer.visualise(phrase)
            elif command in ['/e', '/encode']:
                tokens = [int(token) for token in phrase.replace(' ','').split(',')]
                print(tokenizer.detokenise(tokens))
            else:
                print("improper command used, try again.")