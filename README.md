# sent-bias

This repository contains the code and data for the paper "[On Measuring Social Biases in Sentence Encoders](https://arxiv.org/abs/1903.10561)" by Chandler May, Alex Wang, Shikha Bordia, Samuel R. Bowman and Rachel Rudinger.

## Setup

### Environment setup

First, install Anaconda and a C++ compiler (for example, `g++`) if you
do not have them.

#### Using the prespecified environment

Use `environment.yml` to create a conda environment with all necessary
code dependencies:

```
conda env create -f environment.yml
```

Activate the environment as follows:

```
source activate sentbias
```

#### Recreating the environment

Alternatively (for example,
if you have problems using the prespecified environment), follow
approximately the following steps to recreate it.  First, create a new
environment with Python 3.6:

```
conda create -n sentbias python=3.6
```

Then activate the environment and add the remaining dependencies:

```
source activate sentbias
conda install pytorch=0.4.1 cuda90 -c pytorch
conda install tensorflow
pip install allennlp gensim tensorflow-hub pytorch-pretrained-bert numpy scipy nltk spacy h5py scikit-learn
```

#### Environment postsetup

Now, with the environment activated, download the NLTK punkt and spacy en
resources:

```
python -c 'import nltk; nltk.download("punkt")'
python -m spacy download en
```

You will also need to download pretrained model weights for each model
you want to test.  Instructions for each supported model are as
follows.

### BERT

BERT weights will be downloaded from [Bert repo](https://github.com/huggingface/pytorch-pretrained-BERT) and cached at runtime.  Set `PYTORCH_PRETRAINED_BERT_CACHE` in your environment to a directory you'd like them to be saved to; otherwise they will be saved to `~/.pytorch_pretrained_bert`.  For example, if using bash, run this before running BERT bias tests or put it in your `~/.bashrc` and start a new shell session to run bias tests:

```
export PYTORCH_PRETRAINED_BERT_CACHE=/data/bert_cache
```

/Users/christine/opt/anaconda3/envs/scripts_sentbias/bin/python /Users/christine/Documents/education/university/Praxisarbeit/PA2/PA2-Code/May2019_sent-bias/sentbias/main.py -m bert --results_path output/german-bert.tsv --ignore_cached_encs

## Running Bias Tests

We provide a script that demonstrates how to run the bias tests for each model.  To use it, minimally set the path to the GloVe vectors as `GLOVE_PATH` in a file called `user_config.sh`:

```
GLOVE_PATH=path/to/glove.840B.300d.txt
```

Then copy `scripts/run_tests.sh` to a temporary location, edit as desired, and run it with `bash`.

### Details

To run bias tests directly, run `main` with one or more tests and one or more models.  Note that each model may require additional command-line flags specifying locations of resources and other options. For example, to run all tests against the bag-of-words (GloVe) and ELMo models:

```
python sentbias/main.py -m bow,elmo --glove_path path/to/glove.840B.300d.txt
```

If they are available, cached sentence representations in the `output` directory will be loaded and used; if they are not available, they will be computed (and cached under `output`).
Run `python sentbias/main.py --help` to see a full list of options.

## Code Tests

To run style checks, first install `flake8`:

```
pip install flake8
```

Then run it as follows:

```
flake8
```

## License

This code is distributed under the Creative Commons
Attribution-NonCommercial 4.0 International license, which can be found
in the `LICENSE` file in this directory.

The file `sentbias/models.py` is based on [`models.py` in InferSent](https://github.com/facebookresearch/InferSent/blob/74990f5f9aa46d2e549eeb7b80bd64dbf338407d/models.py) with small modifications by us (May, Wang, Bordia, Bowman, and Rudinger); the original file is copyright Facebook, Inc. under the Creative Commons Attribution-NonCommercial 4.0 International license.