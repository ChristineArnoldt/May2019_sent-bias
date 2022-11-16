# This is a list of partial commands to run to regenerate all results
# in the paper.  It's designed to be used with GNU Parallel (or xargs):
#
# sed '/^#/d' scripts/tasks.sh | shuf | parallel --bar --line-buffer -j 2 \
#     {} \
#     --use_cpu \
#     --glove_path /media/cjmay/Data1/sent-bias/glove.840B.300d.txt \
#     --glove_h5_path /media/cjmay/Data1/sent-bias/glove.840B.300d.h5 \
#     --infersent_dir /media/cjmay/Data1/sent-bias/infersent \
#     --gensen_dir /media/cjmay/Data1/sent-bias/gensen \
#     --openai_encs /media/cjmay/Data1/sent-bias/ckpts/jiant/sentbias-openai/openai
#
# That command strips the commented-out lines from this file, shuffles
# the remaining lines, and runs them in parallel (two at a time),
# passing six additional command-line flags to each one.
python sentbias/main.py -m bert --log_file log.bert-1 --results_path results.tsv.bert-1 --bert_version bert-base-uncased
python sentbias/main.py -m bert --log_file log.bert-2 --results_path results.tsv.bert-2 --bert_version bert-large-uncased
python sentbias/main.py -m bert --log_file log.bert-3 --results_path results.tsv.bert-3 --bert_version bert-large-cased
python sentbias/main.py -m bert --log_file log.bert-4 --results_path results.tsv.bert-4 --bert_version bert-base-cased
