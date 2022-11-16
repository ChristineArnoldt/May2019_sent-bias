#!/bin/bash

source user_config.sh

echo 'Note: this script should be called from the root of the repository' >&2

TESTS=weat1-de,weat6-de,weat6b-de,weat7-de,weat7b-de,weat8-de,weat8b-de,sent-weat1-de,sent-weat6-de,sent-weat6b-de,sent-weat7-de,sent-weat7b-de,sent-weat8-de,sent-weat8b-de,basic-heilman_double_bind_competent_one_word-de, basic-heilman_double_bind_likable_one_word-de, short_ambig-heilman_double_bind_competent_one_word-de, short_ambig-heilman_double_bind_likable_one_word-de, short_clear-heilman_double_bind_competent_one_word-de, short_clear-heilman_double_bind_likable_one_word-de, medium-heilman_double_bind_competent_one_word-de, medium-heilman_double_bind_likable_one_word-de, long_ambig-heilman_double_bind_competent_one_word-de, long_ambig-heilman_double_bind_likable_one_word-de, long_clear-heilman_double_bind_competent_one_word-de, long_clear-heilman_double_bind_likable_one_word-de
#TESTS=weat1
set -e

SEED=1111

# debug
#python ipdb sentbias/main.py --log_file ${SAVE_DIR}/log.log -t ${TESTS} -m bert --bert_version large --exp_dir ${SAVE_DIR} --data_dir tests/ --glove_path ${GLOVE_PATH} --combine_method max 

# BoW (consumes GloVe method)
#python sentbias/main.py --log_file ${SAVE_DIR}/log.log -t ${TESTS} --exp_dir ${SAVE_DIR} --data_dir tests/ -m bow --glove_path ${GLOVE_PATH} -s ${SEED} --ignore_cached_encs

# BERT
#python sentbias/main.py --log_file ${SAVE_DIR}/log.log -t ${TESTS} -m bert --bert_version large --exp_dir ${SAVE_DIR} --data_dir tests/ --glove_path ${GLOVE_PATH} -s ${SEED} --ignore_cached_encs
#python sentbias/main.py --log_file ${SAVE_DIR}/log.log -t ${TESTS} -m bert --bert_version base --exp_dir ${SAVE_DIR} --data_dir tests/ --glove_path ${GLOVE_PATH} -s ${SEED} --ignore_cached_encs

