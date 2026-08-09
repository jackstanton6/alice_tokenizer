import regex
import tqdm
import os
import json
import random
from collections import Counter
from itertools import islice
from math import ceil

GPT2_PAT = r"""'s|'t|'re|'ve|'m|'ll|'d| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""

def numberise(text: str) -> list[int]:
    if not isinstance(text, str):
        raise ValueError(f"str not provided. {type(text)} provided instead")
    char_list = list(text)
    out = [ord(char) for char in char_list]
    return out

def chunk_text(text: str, chunk_num: int) -> list[str]:
    char_num = len(text)
    chunk_size = int(char_num / chunk_num)
    it = iter(text)
    train_chunks = [list(islice(it, chunk_size)) for _ in range((len(train) + chunk_size -1 ) // chunk_size)]
    return train_chunks

def apply_vocab(numbers: list, vocab: dict) -> list:
    current = numbers
    while True:
        out = []
        i = 0
        merged = False
        while i < len(current):
            if i < len(current) - 1 and (current[i], current[i+1]) in vocab:
                out.append(vocab[(current[i], current[i+1])])
                i += 2
                merged = True
            else:
                out.append(current[i])
                i += 1
        current = out
        if not merged:
            break
    return current

def test(vocab):
    print("alice")

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

    data_chunks = chunk_text(data, chunks)
    THRESHOLD = ceil(vocab_size / chunks) # pairs to consider

    top = 200 # where to start with new vocab entry codes
    vocab = {}

    if not quiet:
        train_chunks = tqdm.tqdm(data_chunks)
    else:
        train_chunks = data_chunks

    for chunk in train_chunks:
        pairs_counter = Counter()
        for article in chunk:
            if pretokenize:
                pieces = regex.findall(GPT2_PAT, article)
            else:
                pieces = [article]

            for piece in pieces:
                bite = apply_vocab(numberise(piece), vocab)
                for i in range(len(bite) - 1):
                    pair = (bite[i], bite[i+1])
                    pairs_counter[pair] += 1

        temp_lol = THRESHOLD

        if THRESHOLD > len(pairs_counter.most_common()): # probably will never trigger, just in case though
            temp_lol = len(pairs_counter.most_common())

        for key, value in pairs_counter.most_common()[:temp_lol]:
            vocab[key] = top
            top += 1

    if not quiet:
        print("Finished training!")
        print(f"Final vocab count: {len(vocab)}")

    if save_to_file:
        if not quiet:
            print("Saving vocab...")
        if save_format != 'json':
            print("Unable to save to non-json format at this time.")
        else:
            serialisable_vocab = {f"{a},{b}": v for (a, b), v in vocab.items()}
            with open(f'{name}.json', "w", encoding="utf-8") as f:
                json.dump(serialisable_vocab, f, indent=4)

    if do_tests:
        test(vocab)
    
    return vocab