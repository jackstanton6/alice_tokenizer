import regex
import tqdm
import json
import random
from collections import Counter
from itertools import islice
from math import ceil

GPT2_PAT = r"""'s|'t|'re|'ve|'m|'ll|'d| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""

test_phrases = [
        "The quick brown fox jumped over the lazy dog.",
        "How much wood could a woodchuck chuck if a wood chuck could chuck wood?",
        '"But man is not made for defeat," he said. "A man can be destroyed but not defeated." I am sorry that I killed the fish though, he thought. Now the bad time is coming and I do not even have the harpoon.',
        "It is a truth universally acknowledged, that a single man in possession of a good fortune must be in want of a wife.\nHowever little known the feelings or views of such a man may be on his first entering a neighbourhood, this truth is so well fixed in the minds of the surrounding families, that he is considered as the rightful property of some one or other of their daughters."
        "I, Ishmael, was one of that crew; my shouts had gone up with the rest; my oath had been welded with theirs; and stronger I shouted, and more did I hammer and clinch my oath, because of the dread in my soul.",
        "Tell me, O Muse, of that ingenious hero who travelled far and wide after he had sacked the famous town of Troy. Many cities did he visit, and many were the nations with whose manners and customs he was acquainted",
        "What is the use that now at this present I make of my soul? Thus from time to time and upon all occasions thou must put this question to thyself; what is now that part of mine which they call the rational mistress part, employed about? Whose soul do I now properly possess? a child's? or a youth's? a woman's? or a tyrant's? some brute, or some wild beast's soul?",
        "Lorem ipsum dolor sit amet consectetur adipiscing elit. Sit amet consectetur adipiscing elit quisque faucibus ex. Adipiscing elit quisque faucibus ex sapien vitae pellentesque.",
        "Purple plump pomegranates fall faster than sailboats sail",
        """current = numbers
while True:
    out = []
    i = 0
    merged = False
    while i < len(current):""",
        "When you were here before. Couldn't look you in the eye. You're just like an angel. Your skin makes me cry. You float like a feather. In a beautiful world. You're so fucking special. I wish I was special. But I'm a creep. I'm a weirdo.",
        "x^2+3x-2=0, x=2,x=-1",
        """Riding home from credulous blue domes,
the dreamer reins his waking appetite
in panic at the crop of catacombs
sprung up like plague of toadstools overnight:
refectories where he reveled have become
the holstery of worms, rapacious blades
who weave within the skeleton's white womb
a caviare decay of rich brocades.""",
        "Chancellor on brink of second bailout for banks."
    ]

def visualise_tokens(self, user_in: str, vocab: dict) -> None:
    tokens = apply_vocab(user_in, vocab)
    lookup = {vocab[key]: key for key in vocab}
    def decode_token(token_id):
        if token_id in lookup:
            a, b = lookup[token_id]
            return decode_token(a) + decode_token(b)
        return chr(token_id)
    repres = []
    for token in tokens:
        repres.append(f"{token}: {decode_token(token)!r}")
    print(', '.join(repres))

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

def test(in_vocab: dict, num_tests: int = 5):
    phrases = test_phrases
    random.shuffle(phrases)
    selected_phrases = phrases[num_tests:]
    for phrase in selected_phrases:
        print(phrase)
        visualise_tokens(phrase, in_vocab)

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

    if do_tests and not quiet:
        test(vocab)
    
    return vocab