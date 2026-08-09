# alice_tokenizer

the alice tokenizer is a project i developed as part of learning about the workings of transformers. this is a tokenizer i built for my own transformer and i decided to release as a standalone application to make building a byte-pair encoder on any dataset easy for anyone.

using alice_tokenizer is easy, it takes only a few steps to install and run.

## installation

you can install alice_tokenizer using pip

```bash
pip install alice_tokenizer
```

## usage

### python

#### tokenizing

tokenizing a string in alice is easy. start by initialising the tokenizer.

```python
import alice_tokenizer as alice

tokenizer = alice.Tokenizer()
```

to turn a string into tokens use the tokenize method.

```python
tokens = tokenizer.tokenize("Tokenize me") # returns a list with integers
```

to turn tokens back into text use the detokenize method.

```python
output = tokenizer.detokenize(tokens) # returns a string
```

for a visual look at how the tokens are split up, use the visualize_tokens method

```python
tokenizer.visualize_tokens(tokens)
tokenizer.visualize_tokens("Tokenize me.") # works on str and token lists
```

#### making a tokenizer

to make a tokenizer, you must have a text file with text data inside. at this juncture alice only supports ascii, although this will be remedied in the future. for now ensure that your file uses utf-8 encoding as it will be read as utf-8.

start by initialising the tokenizer with the build=True condition.

```python
import alice_tokenizer as alice

tokenizer = alice.Tokenizer(build=True)
```

then declare your text file (it is recommended to use a dataset of at least 20mb or larger, the larger the better).

```python
tokenizer.set_data('data.txt')
```

then begin training

```python
tokenizer.train(
    vocab_size = 32_000,
    chunks = 4_000,
    name = 'bob',
    save_format = 'json',
    save_to_file = True,
    pretokenize = True,
    do_tests = True,
    quiet = False
)
```

below is a description of each parameter
* *vocab_size*: how large the resultant vocabulary should be. for a standard english tokenizer 32k is the recommended size but it can be as large or as small as you wish.
* *chunks*: how many chunks the training data should be split into. ensure it is a factor of vocab_size to ensure that the exact vocab size is met.
* *name*: the name of the tokenizer to save afterwards. when the vocabulary is saved to a file, this is the filename it will use.
* *save_format*: the format of the final vocabulary file. only json is supported as of now, so don't change this
* *save_to_file*: if False, the final vocab won't be saved to the disk after training.
* *pretokenize*: if True, applys the GPT-2 pretokenization pattern to the text before tokenizing.
* *do_tests*: if True, will perform some tests on selected excerpts from the training data after training is complete.
* *quiet*: if True, will not print anything during training

these values are all the preset defaults, if not declared they will snap back to these defaults instead.

once the tokenizer is done building, you can test it immediately by using the tokenizer object methods.

```python
tokens = tokenizer.tokenize("Tokenize me.")
output = tokenizer.detokenize(tokens)
tokenizer.visualize_tokens(tokens)
tokenizer.visualize_tokens("Tokenize me.")
```

to load your vocab into alice again, you can declare the vocab file when initialising the tokenizer

```python
import alice_tokenizer as alice

tokenizer = alice.Tokenizer(vocab_file="bob.json")
```