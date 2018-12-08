#!/usr/bin/env python3

from csv import DictReader


STAR_THRESHOLD = 0.01
SINGLE_STAR = r'^{*\phantom{*}}'
DOUBLE_STAR = r'^{**}'
STAR_SPACE = r'\phantom{^{**}}'

SIGNIFICANT_FIGURES = 2

CTX_WORD = 'word'
CTX_SENT = 'sentence'
CTX_PARA = 'paragraph'

MODELS = (
    ('bow', ''),
    ('infersent', ''),
    ('gensen', 'version=nli_large_bothskip_parse,nli_large_bothskip'),
    ('guse', ''),
    ('elmo', 'time_combine=mean;layer_combine=add'),
    (None, None),
    ('bert', 'version=bert-large-cased'),
)

TESTS = (
    ('weat1', 'C1: Flowers/Insects', CTX_WORD),
    ('sent-weat1', 'C1: Flowers/Insects', CTX_SENT),
    ('weat2', 'C2: Instruments/Weapons', CTX_WORD),
    ('sent-weat2', 'C2: Instruments/Weapons', CTX_SENT),
    ('weat3', 'C3: EA/AA Names', CTX_WORD),
    ('sent-weat3', 'C3: EA/AA Names', CTX_SENT),
    ('weat6', 'C6: M/F Names, Career', CTX_WORD),
    ('sent-weat6', 'C6: M/F Names, Career', CTX_SENT),
    (None, None, None),
    ('angry_black_woman_stereotype', 'Angry Black Woman', CTX_WORD),
    ('sent-angry_black_woman_stereotype', 'Angry Black Woman', CTX_SENT),
    (None, None, None),
    ('heilman_double_bind_competent_one_word', 'Double Bind: Competent', CTX_WORD),
    ('heilman_double_bind_competent_one_sentence', 'Double Bind: Competent', CTX_SENT),
    ('heilman_double_bind_competent_1-', 'Double Bind: Competent', CTX_PARA),
    ('heilman_double_bind_likable_one_word', 'Double Bind: Likable', CTX_WORD),
    ('heilman_double_bind_likable_one_sentence', 'Double Bind: Likable', CTX_SENT),
    ('heilman_double_bind_likable_1-', 'Double Bind: Likable', CTX_PARA),
)


def main():
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(
        'Read results from tsv file and print out rows for LaTeX table.',
        formatter_class=ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('results_path',
                        help='Paths to results tsv file.')
    args = parser.parse_args()

    results = dict()
    with open(args.results_path) as f:
        reader = DictReader(f, delimiter='\t')
        for row in reader:
            for k in ('p_value', 'effect_size'):
                row[k] = float(row[k])
            for k in ('num_targ1', 'num_targ2', 'num_attr1', 'num_attr2'):
                row[k] = int(row[k])

            k = (row['model'], row['options'], row['test'])
            if k in results:
                raise Exception('duplicate key: {}'.format(k))
            results[k] = row

    results_list = sorted(results.items(), key=lambda p: p[1]['p_value'])
    reject = True
    for (i, (k, row)) in enumerate(results_list):
        if row['p_value'] > STAR_THRESHOLD / (len(results_list) - i):
            reject = False
        row['reject'] = reject

    for (test_name, test_description, context_level) in TESTS:
        if test_name is None:
            print('\n\\midrule\n')
        else:
            print('{} & {}'.format(test_description, context_level), end='')
            for (model, options) in MODELS:
                if model is None:
                    print(' & ', end='')
                else:
                    row = results[(model, options, test_name)]
                    effect_size = row['effect_size']
                    star = DOUBLE_STAR if row['reject'] else (
                        SINGLE_STAR if row['p_value'] <= STAR_THRESHOLD else STAR_SPACE
                    )
                    print(' & ${effect_size:.{precision}f}{star}$'.format(
                        effect_size=effect_size,
                        star=star,
                        precision=SIGNIFICANT_FIGURES), end='')
            print(' \\\\')


if __name__ == '__main__':
    main()