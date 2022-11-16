''' Main script for loading models and running WEAT tests '''

import os
import sys
import random
import re
import argparse
import logging as log
log.basicConfig(format='%(asctime)s: %(message)s', datefmt='%m/%d %I:%M:%S %p', level=log.INFO)  # noqa

from csv import DictWriter
from enum import Enum

import numpy as np

from data import (
    load_json, load_encodings, save_encodings,
)
import weat
import encoders.bert as bert


class ModelName(Enum):
    BERT = 'bert'

TEST_EXT = '.jsonl'
MODEL_NAMES = [m.value for m in ModelName]
BERT_VERSIONS = ["bert-base-german-cased","dbmdz/bert-base-german-cased","Geotrend/bert-base-de-cased"]


def test_sort_key(test):
    '''
    Return tuple to be used as a sort key for the specified test name.
   Break test name into pieces consisting of the integers in the name
    and the strings in between them.
    '''
    key = ()
    prev_end = 0
    for match in re.finditer(r'\d+', test):
        key = key + (test[prev_end:match.start()], int(match.group(0)))
        prev_end = match.end()
    key = key + (test[prev_end:],)

    return key


def handle_arguments(arguments):
    ''' Helper function for handling argument parsing '''
    parser = argparse.ArgumentParser(
        description='Run specified SEAT tests on specified models.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--tests', '-t', type=str,
                        help="WEAT tests to run (a comma-separated list; test files should be in `data_dir` and "
                             "have corresponding names, with extension {}). Default: all tests.".format(TEST_EXT))
    parser.add_argument('--models', '-m', type=str,
                        help="Models to evaluate (a comma-separated list; options: {}). "
                             "Default: all models.".format(','.join(MODEL_NAMES)))
    parser.add_argument('--seed', '-s', type=int, help="Random seed", default=1111)
    parser.add_argument('--log_file', '-l', type=str,
                        help="File to log to")
    parser.add_argument('--results_path', type=str,
                        help="Path where TSV results file will be written")
    parser.add_argument('--ignore_cached_encs', '-i', action='store_true',
                        help="If set, ignore existing encodings and encode from scratch.")
    parser.add_argument('--dont_cache_encs', action='store_true',
                        help="If set, don't cache encodings to disk.")
    parser.add_argument('--data_dir', '-d', type=str,
                        help="Directory containing examples for each test",
                        default='tests')
    parser.add_argument('--exp_dir', type=str,
                        help="Directory from which to load and save vectors. "
                             "Files should be stored as h5py files.",
                        default='output')
    parser.add_argument('--n_samples', type=int,
                        help="Number of permutation test samples used when estimate p-values (exact test is used if "
                             "there are fewer than this many permutations)",
                        default=100000)
    parser.add_argument('--parametric', action='store_true',
                        help='Use parametric test (normal assumption) to compute p-values.')
    parser.add_argument('--use_cpu', action='store_true',
                        help='Use CPU to encode sentences.')
    bert_group = parser.add_argument_group(ModelName.BERT.value, 'Options for BERT model')
    bert_group.add_argument('--bert_version', type=str, choices=BERT_VERSIONS,
                            help="Version of BERT to use.", default="bert-base-german-cased")

    return parser.parse_args(arguments)


def split_comma_and_check(arg_str, allowed_set, item_type):
    ''' Given a comma-separated string of items,
    split on commas and check if all items are in allowed_set.
    item_type is just for the assert message. '''
    items = arg_str.split(',')
    for item in items:
        if item not in allowed_set:
            raise ValueError("Unknown %s: %s!" % (item_type, item))
    return items


def maybe_make_dir(dirname):
    ''' Maybe make directory '''
    os.makedirs(dirname, exist_ok=True)


def main(arguments):
    ''' Main logic: parse args for tests to run and which models to evaluate '''
    log.basicConfig(format='%(asctime)s: %(message)s', datefmt='%m/%d %I:%M:%S %p', level=log.INFO)

    args = handle_arguments(arguments)
    if args.seed >= 0:
        log.info('Seeding random number generators with {}'.format(args.seed))
        random.seed(args.seed)
        np.random.seed(args.seed)
    maybe_make_dir(args.exp_dir)
    if args.log_file:
        log.getLogger().addHandler(log.FileHandler(args.log_file))
    log.info("Parsed args: \n%s", args)

    all_tests = sorted(
        [
            entry[:-len(TEST_EXT)]
            for entry in os.listdir(args.data_dir)
            if not entry.startswith('.') and entry.endswith(TEST_EXT)
        ],
        key=test_sort_key
    )
    log.debug('Tests found:')
    for test in all_tests:
        log.debug('\t{}'.format(test))

    tests = split_comma_and_check(args.tests, all_tests, "test") if args.tests is not None else all_tests
    log.info('Tests selected:')
    for test in tests:
        log.info('\t{}'.format(test))

    models = split_comma_and_check(args.models, MODEL_NAMES, "model") if args.models is not None else MODEL_NAMES
    log.info('Models selected:')
    for model in models:
        log.info('\t{}'.format(model))


    results = []
    for model_name in models:
        # Different models have different interfaces for things, but generally want to:
        # - if saved vectors aren't there:
        #    - load the model
        #    - load the test data
        #    - encode the vectors
        #    - dump the files into some storage
        # - else load the saved vectors '''
        log.info('Running tests for model {}'.format(model_name))


        if model_name == ModelName.BERT.value:
            model_options = 'version=' + args.bert_version
        else:
            raise ValueError("Model %s not found!" % model_name)

        model = None

        for test in tests:
            log.info('Running test {} for model {}'.format(test, model_name))
            enc_file = os.path.join(args.exp_dir, "%s.%s.h5" % (
                "%s;%s" % (model_name, model_options) if model_options else model_name,
                test))
            if not args.ignore_cached_encs and os.path.isfile(enc_file):
                log.info("Loading encodings from %s", enc_file)
                encs = load_encodings(enc_file)
                encs_targ1 = encs['targ1']
                encs_targ2 = encs['targ2']
                encs_attr1 = encs['attr1']
                encs_attr2 = encs['attr2']
            else:
                # load the test data
                encs = load_json(os.path.join(args.data_dir, "%s%s" % (test, TEST_EXT)))

                # load the model and do model-specific encoding procedure
                log.info('Computing sentence encodings')
                if model_name == ModelName.BERT.value:
                    model, tokenizer = bert.load_model(args.bert_version)
                    encs_targ1 = bert.encode(model, tokenizer, encs["targ1"]["examples"])
                    encs_targ2 = bert.encode(model, tokenizer, encs["targ2"]["examples"])
                    encs_attr1 = bert.encode(model, tokenizer, encs["attr1"]["examples"])
                    encs_attr2 = bert.encode(model, tokenizer, encs["attr2"]["examples"])
                else:
                    raise ValueError("Model %s not found!" % model_name)

                encs["targ1"]["encs"] = encs_targ1
                encs["targ2"]["encs"] = encs_targ2
                encs["attr1"]["encs"] = encs_attr1
                encs["attr2"]["encs"] = encs_attr2

                log.info("\tDone!")
                if not args.dont_cache_encs:
                    log.info("Saving encodings to %s", enc_file)
                    save_encodings(encs, enc_file)

            enc = [e for e in encs["targ1"]['encs'].values()][0]
            d_rep = enc.size if isinstance(enc, np.ndarray) else len(enc)

            # run the test on the encodings
            log.info("Running SEAT...")
            log.info("Representation dimension: {}".format(d_rep))
            esize, pval = weat.run_test(encs, n_samples=args.n_samples, parametric=args.parametric)
            results.append(dict(
                model=model_name,
                options=model_options,
                test=test,
                p_value=pval,
                effect_size=esize,
                num_targ1=len(encs['targ1']['encs']),
                num_targ2=len(encs['targ2']['encs']),
                num_attr1=len(encs['attr1']['encs']),
                num_attr2=len(encs['attr2']['encs'])))

        log.info("Model: %s", model_name)
        log.info('Options: {}'.format(model_options))
        for r in results:
            log.info("\tTest {test}:\tp-val: {p_value:.9f}\tesize: {effect_size:.2f}".format(**r))

    if args.results_path is not None:
        log.info('Writing results to {}'.format(args.results_path))
        with open(args.results_path, 'w') as f:
            writer = DictWriter(f, fieldnames=results[0].keys(), delimiter='\t')
            writer.writeheader()
            for r in results:
                writer.writerow(r)


if __name__ == "__main__":
    main(sys.argv[1:])
