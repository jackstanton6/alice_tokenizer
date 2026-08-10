import json

from .util.vocab import vocab as alice_vocab
from .util.logo import logo
from .train_tokeniser import train

class Tokeniser:
    def __init__(
            self,
            name: str = 'alice_zero',
            build: bool = False,
            vocab_file: str | None = None,
            vocab: dict | None = None
        ):
        self.name = name
        self.build = build
        if vocab is not None:
            self.encoding = vocab
            self.vocab_size = len(self.encoding)
        elif not build:
            self.encoding = {(int(key.split(',')[0]), int(key.split(',')[1])): alice_vocab[key] for key in alice_vocab}
            self.vocab_size = len(self.encoding)

    def set_data(self, filename: str):
        if not self.build:
            raise ValueError("Tokeniser not in build mode, cannot set data.")
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = ' '.join(f.readlines())
                self.data = data.encode('ascii', 'ignore').decode('ascii')
        except:
            raise FileNotFoundError("Data file not found, ensure it")

    def train(self,
            vocab_size: int = 32_000,
            chunks: int = 4_000,
            name: str = 'bob',
            save_format: str = 'json',
            save_to_file: bool = True,
            pretokenize: bool = True,
            do_tests: bool = True,
            quiet: bool = False
        ):
        if not self.build:
            raise ValueError("Tokeniser not in build mode, cannot train tokeniser.")
        if self.data is None:
            raise ValueError("Data has not been loaded. Please load data with set_data('filename.txt')")
        if not quiet:
            print(logo)
            print("Beginning tokeniser fit.")
            print(f"Vocab Target: {vocab_size}, Data Size: {len(self.data)}")
        self.encoding = train(
            self.data, 
            vocab_size=vocab_size,
            chunks=chunks,
            name=name,
            save_format=save_format,
            save_to_file=save_to_file,
            pretokenize=pretokenize,
            do_tests=do_tests,
            quiet=quiet
        )
        self.build = False
        self.tokeniser = 'name'
        self.vocab_size = vocab_size

    def tokenize(self, text_in: str) -> list[int]:
        return self.tokenise(text_in)

    def tokenise(self, text_in: str) -> list[int]:
        if self.build:
            raise AssertionError("Tokeniser is currently in build mode. Finish building the tokeniser before trying to tokenise.")
        if not isinstance(text_in, str):
            raise ValueError(f"String input is required, non string {type(text_in)} provided.")
        if text_in == "":
            raise ValueError("Empty string.")
        current = [ord(char) for char in text_in]
        while True:
            out = []
            i = 0
            merged = False
            while i < len(current):
                if i < len(current) - 1 and (current[i], current[i+1]) in self.encoding:
                    out.append(self.encoding[(current[i], current[i+1])])
                    i += 2
                    merged = True
                else:
                    out.append(current[i])
                    i += 1
            current = out
            if not merged:
                break
        return current

    def visualise(self, tokens: list[int] | str) -> None:
        self.visualise_tokens(tokens)

    def visualize_tokens(self, tokens: list[int] | str) -> None:
        self.visualise_tokens(tokens)

    def visualise_tokens(self, tokens: list[int] | str) -> None:
        if self.build:
            raise AssertionError("Tokeniser is currently in build mode. Finish building the tokeniser before trying to tokenise.")
        if isinstance(tokens, str):
            tokens = self.tokenise(tokens)
        if not isinstance(tokens, list) or not all(isinstance(token, int) for token in tokens):
            raise ValueError("Input is not a list of tokens.")
        lookup = {self.encoding[key]: key for key in self.encoding}
        def decode_token(token_id):
            if token_id in lookup:
                a, b = lookup[token_id]
                return decode_token(a) + decode_token(b)
            return chr(token_id)
        repres = []
        for token in tokens:
            repres.append(f"{token}: {decode_token(token)!r}")
        print(', '.join(repres))

    def detokenise(self, tokens: list[int]) -> list:
        if self.build:
            raise AssertionError("Tokeniser is currently in build mode. Finish building the tokeniser before trying to tokenise.")
        if not isinstance(tokens, list) or not all(isinstance(token, int) for token in tokens):
            raise ValueError("Input is not a list of tokens.")
        lookup = {self.encoding[key]: key for key in self.encoding}
        current = tokens
        while not all(n < 200 for n in current):
            out = []
            for token in current:
                if token in lookup:
                    out.append(lookup[token][0])
                    out.append(lookup[token][1])
                else:
                    out.append(token)
            current = out
        return ''.join(chr(n) for n in current)