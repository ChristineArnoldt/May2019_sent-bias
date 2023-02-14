# sent-bias-german

This is an adaptation of the code for the paper "[On Measuring Social Biases in Sentence Encoders](https://arxiv.org/abs/1903.10561)" by Chandler May, Alex Wang, Shikha Bordia, Samuel R. Bowman and Rachel Rudinger to measure gender bias in german BERT.
The original code can be found here: https://github.com/W4ngatang/sent-bias


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
source activate sentbias_german
```

#### Recreating the environment

Alternatively (for example, if you have problems using the prespecified environment), follow
approximately the following steps to recreate it.  First, create a new
environment with Python 3.8:

```
conda create -n sentbias_german python=3.8
```

Then activate the environment and add the remaining dependencies:

```
source activate sentbias_german
#conda install pytorch=0.4.1 cuda90 -c pytorch
conda install tensorflow
pip install allennlp gensim tensorflow-hub || numpy scipy nltk spacy h5py scikit-learn || german_nouns ttictoc gender-determinator Levenshtein
```

#### Environment postsetup

Now, with the environment activated, download the NLTK punkt and spacy en
resources:

```
python -c 'import nltk; nltk.download("punkt")'
python -m spacy download de
```

## Running Bias Tests

Scripts should always be run from the scripts directory.
The tests are run by running main with the flags:
```
-m bert --results_path output/german-bert.tsv --ignore_encs
```
For more information on the flags and other options refer to the help using `-h` when running `main`.

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
