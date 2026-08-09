from ..util.logo import logo
from ..tokenisation import *

def main():
    print(logo)
    tokeniser = Tokeniser()
    while True:
        user_in = input("> ")
        print(tokeniser.tokenise(user_in))