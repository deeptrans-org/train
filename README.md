# DeepTrans

Easy to use, cross-platform toolkit to train [deeptrans-train](https://github.com/wildwolf085/deamtrans-train) models, which can be used by [deeptrans](https://deamtrans.org) 🚂

## Requirements

 * Python == 3.11
 * NVIDIA CUDA graphics card (not required, but highly recommended)

## Install

```bash
git clone https://github.com/deeptrans-org/train.git
cd train
pip install -r requirements.txt

# compile tools
g++ -g tool_validate.cpp -o validate
# build release mode

# install gcc
# download https://github.com/niXman/mingw-builds-binaries/releases/download/14.2.0-rt_v12-rev2/x86_64-14.2.0-release-posix-seh-ucrt-rt_v12-rev2.7z
g++ -O3 -fopenmp tool_shuffle.cpp -o shuffle

./shuffle en it 0 1000
```

## Background

Language models can be trained by providing lots of example translations from a source language to a target language. All you need to get started is a set of two files (`{source_code}` and `target_code`). The source file containing sentences written in the source language and a corresponding file with sentences written in the target language.

For example:

`primary.en`:

```
Hello
Goodbye
```

`primary.it`:

```
Ciao
Arrivederci
```

## Usage

Place `primary.en` and `primary.it` files in ".\corpora" folder:

```bash
corpora/
├── primary.en
└── primary.it
```

Then run:

```bash
python train.py en it

# [en] can be omitted.
python train.py it
```

Training can take a while and depending on the size of datasets can require a graphics card with lots of memory.

The output will be saved in `run/[from]-[to]-[YYMM].[vocab_size(k)].[input_size(gb)]` 
ex: `run/en-it-250402.50.16.dp` (Trained on April 2, 2025 with 32,000 vocabularies and 16 GB corpus size).

### Reverse Training

Once you have trained a model from `source => target`, you can easily train a reverse model `target => source` model by passing `--reverse`:

```bash
python train.py en it --reverse
# [en] can be omitted.
python train.py it --reverse
```

## Contribute

Want to share your model with the world? Post it on [community.deeptrans.org](https://community.deeptrans.org) and we'll include in future releases of DeepTrans. 
Make sure to share both a forward and reverse model (e.g. `en => it` and `it => en`), otherwise we won't be able to include it in the model repository.

We also welcome contributions to DeepTrans! Just open a pull request.

## Credits

In no particular order, we'd like to thank:

 * [OpenNMT-py](https://github.com/OpenNMT/OpenNMT-py)
 * [SentencePiece](https://github.com/google/sentencepiece)
 * [OPUS](https://opus.nlpl.eu)

For making DeepTrans possible.

## License

AGPLv3