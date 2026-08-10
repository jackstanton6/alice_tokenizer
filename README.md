# alice_tokenizer

the alice tokenizer is a project i developed as part of learning about the workings of transformers. this is a tokenizer i built for my own transformer and i decided to release as a standalone application to make building a byte-pair encoder on any dataset easy for anyone.

using alice_tokenizer is easy, it takes only a few steps to install and run.

## installation

you can install alice_tokenizer using pip

```bash
pip install alice-tokenizer
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

once the tokenizer is done building, you can use it immediately by using the tokenizer object methods.

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

### command line

when installing the alice tokenizer, it comes with a nifty command line tool to allow you to more easily interface with the alice tokenizer without needing to use python.

to boot it up, simply run

```bash
$ alice_t
```

this will open alice_t's terminal window, allowing you to enter in text and get back the tokenization instantly. to see everything you can do with alice_t, run the `/help` command when using it.

#### training in the command line

to train on the command line, you must pass the `--train` argument when using alice_t. this tells the program to begin training the tokenizer. you must pass the filename of your training data with `--data_file` to begin training, or else the training will not be able to start.

example of a minimal training command

```bash
$ alice_t --train --data_file train.txt
```

this will begin training, once done it will open a terminal where you can use the newly trained tokenizer.
using this command will negate many of the benefits using alice_tokenizer can give you. it wont save to your disk, have a name, nor can you declare the target vocab size. to do so you can use other arguments to declare these parameters.

```bash
$ alice_t --train --data_file train.txt --vocab_size 32000 --chunks 8000 --name bob --format json --save_to_file --pretokenize --do_tests
```

these parameters have the same function as the train() command does. if one is not included, it will snap back to its default. if --save_to_file, --pretokenize or --do_tests are not included, they will default to False. to see a list of each argument, use `alice_t --help`.