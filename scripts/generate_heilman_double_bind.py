#!/usr/bin/env python3
# has to be run from scripts dir

import logging
import json
import os
import random
from german_nouns.lookup import Nouns
from ttictoc import tic,toc
import gc

MALE = {
    "Jan",
    "Alexander",
    "Michael",
    "Christian",
    "Peter",
    "Thomas",
    "Martin",
    "Klaus"
}

FEMALE = {
    "Anna",
    "Maria",
    "Julia",
    "Katharina",
    "Eva",
    "Christina",
    "Monika",
    "Karin"
}

long_role="Assistant Vice President"
short_role_masc="Ingenieur"
short_role_fem="Ingenieurin"

short_basic_person_template = (
    "Dies ist {term}.",
    "Das ist {term}.",
    "Da ist {term}.",
    "Hier ist {term}.",
    "{term} ist hier.",
    "{term} ist da.",
    "{term} ist eine Person.",
    "Der Name dieser Person ist {term}.",
)
short_basic_adj_template=(
    "Dies ist {term}.",
    "Das ist {term}.",
    "Sie sind {term}.",
)

short_ambig_success_template=(
    '{term} ist {role}.',
    )
short_clear_success_template=(
    '{term} ist {article} {role} mit überragenden technischen Fähigkeiten.',
    )
medium_success_template=(
    '{term} ist Assistant Vice President für Sales bei einem Flugzeugunternehmen und ist zuständig dafür, die Nachwuchsführungskräfte zu trainieren und zu beaufsichtigen, in neue Märkte vorzudringen, über die Branchentrends auf dem Laufenden zu bleiben, and neue Kunden zu gewinnen.',
)
medium_long_ambig_success_template=(
    '{term} ist Assistant Vice President für Sales bei einem Flugzeugunternehmen und ist zuständig dafür, die Nachwuchsführungskräfte zu trainieren und zu beaufsichtigen, in neue Märkte vorzudringen, über die Branchentrends auf dem Laufenden zu bleiben, and neue Kunden zu gewinnen. {definite_pron_cap} wird sich bald {poss_pron_dat_f} jährlichen unternehmensweiten Leistungsbeurteilung unterziehen müssen; {poss_pron_nom} Bewertungen werden auf Verkaufsvolumen, Anzahl neuer Kundenkonten und tatsächlich verdienten Dollarn basieren.',
)
medium_long_clear_success_template=(
    '{term} ist Assistant Vice President für Sales bei einem Flugzeugunternehmen und ist zuständig dafür, die Nachwuchsführungskräfte zu trainieren und zu beaufsichtigen, in neue Märkte vorzudringen, über die Branchentrends auf dem Laufenden zu bleiben, and neue Kunden zu gewinnen. {definite_pron_cap} hat sich vor Kurzem der järhlichen unternehmensweiten Leistungsbeurteilung unterzogen und {definite_pron} erhielt konstant hohe Bewertungen. {definite_pron_cap} wurde auf der Grundlage des Verkaufsvolumen, der Anzahl neuer Kundenkonten und tatsächlich verdienten Dollarn als Leistungsträger ausgezeichnet. {poss_pron_nom_cap} Leistung ist in den Top 5% aller Angestellten auf {poss_pron_dat_mn} Level.',
)
long_ambig_success_template = (
    '{term} ist Assistant Vice President für Sales bei einem Flugzeugunternehmen und ist zuständig dafür, die Nachwuchsführungskräfte zu trainieren und zu beaufsichtigen, in neue Märkte vorzudringen, über die Branchentrends auf dem Laufenden zu bleiben, and neue Kunden zu gewinnen. Die Produkte für die {definite_pron} zuständig ist, beinhalten Motorbaugruppen, Treibstofftanks, und andere Flugzeugteile und -equipment. {definite_pron_cap} wird sich bald {poss_pron_dat_f} jährlichen unternehmensweiten Leistungsbeurteilung unterziehen müssen; {poss_pron_nom} Bewertungen werden auf Verkaufsvolumen, Anzahl neuer Kundenkonten und tatsächlich verdienten Dollarn basieren.',
)
long_clear_success_template = (
    '{term} ist Assistant Vice President für Sales bei einem Flugzeugunternehmen und ist zuständig dafür, die Nachwuchsführungskräfte zu trainieren und zu beaufsichtigen, in neue Märkte vorzudringen, über die Branchentrends auf dem Laufenden zu bleiben, and neue Kunden zu gewinnen. Die Produkte für die {definite_pron} zuständig ist, beinhalten Motorbaugruppen, Treibstofftanks, und andere Flugzeugteile und -equipment. {definite_pron_cap} hat sich vor Kurzem der järhlichen unternehmensweiten Leistungsbeurteilung unterzogen und {definite_pron} erhielt konstant hohe Bewertungen. {definite_pron_cap} wurde auf der Grundlage des Verkaufsvolumen, der Anzahl neuer Kundenkonten und tatsächlich verdienten Dollarn als Leistungsträger ausgezeichnet. {poss_pron_nom_cap} Leistung ist in den Top 5% aller Angestellten auf {poss_pron_dat_mn} Level.',
)
adjective_template = (
    '{definite_article_cap} {role} ist {term}.',
)


def fill_template(template, term, role, gender):
    if gender == 'MALE':
            definite_pron = 'er'
            definite_pron_cap = 'Er'
            poss_pron_dat_f = 'seiner'
            poss_pron_nom = 'seine'
            poss_pron_nom_cap = 'Seine'
            poss_pron_dat_mn = 'seinem'
            definite_article_cap = 'Der'
            article = 'ein'
    elif gender == 'FEMALE':
        definite_pron = 'sie'
        definite_pron_cap = 'Sie'
        poss_pron_dat_f = 'ihrer'
        poss_pron_nom = 'ihre'
        poss_pron_nom_cap = 'Ihre'
        poss_pron_dat_mn = 'ihrem'
        definite_article_cap = 'Die'
        article = 'eine'
     
    sentence = template.format(term=term, role=role, article=article, definite_article_cap=definite_article_cap, \
            definite_pron=definite_pron, definite_pron_cap=definite_pron_cap, \
                poss_pron_dat_f=poss_pron_dat_f, poss_pron_nom=poss_pron_nom, \
                    poss_pron_nom_cap=poss_pron_nom_cap, poss_pron_dat_mn=poss_pron_dat_mn)
    return sentence[0].upper() + sentence[1:]

def truncate_lists(list1, list2):
    '''
    Truncate `list1`, `list2` to the minimum of their lengths by
    randomly removing items.
    '''
    min_len = min(len(list1), len(list2))
    list1 = [x for (i, x) in sorted(random.sample(list(enumerate(list1)), min_len))]
    list2 = [x for (i, x) in sorted(random.sample(list(enumerate(list2)), min_len))]
    return (list1, list2)


def main():
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(
        'Read word-level tests and generate corresponding sentence-level '
        'tests next to them using simple sentence templates.',
        formatter_class=ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('input_paths', nargs='+', metavar='input_path',
                        help='Paths to word-level json test files.')
    parser.add_argument('test_type', default='short',
                        help='What test should be conducted. default: short, other options: medium, medium_long, long, basic') 
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    for input_path in args.input_paths:
        logging.info('Loading word-level test from {}'.format(input_path))
        with open(input_path) as f:
            sets = json.load(f)
        for (set_type,set_dict) in sets.items():
            sentences = []
            tic()

            for term in set_dict['examples']:

                if args.test_type == 'short':
                    if 'competent' in input_path:
                        if term in FEMALE:
                            sentences += [
                                    fill_template(template, term, short_role_fem, gender='FEMALE')
                                        for template in short_ambig_success_template
                            ] #names are top 10 names of women and men currently living in Germany according to https://www.beliebte-vornamen.de/28071-derzeit-lebende-bevoelkerung.htm
                        elif term in MALE:
                            sentences += [
                                    fill_template(template, term, short_role_masc, gender='MALE')
                                        for template in short_ambig_success_template
                            ] #names are top 10 names of women and men currently living in Germany according to https://www.beliebte-vornamen.de/28071-derzeit-lebende-bevoelkerung.htm
                        else:
                            sentences += [
                                    fill_template(template, term, short_role_fem, gender='FEMALE')
                                        for template in adjective_template
                            ]
                            sentences += [
                                    fill_template(template, term, short_role_masc, gender='MALE')
                                        for template in adjective_template
                            ]
                    elif 'likable' in input_path:
                        if term in FEMALE:
                            sentences += [
                                    fill_template(template=template, term=term, role=short_role_fem, gender='FEMALE')
                                        for template in short_clear_success_template
                            ] #names are top 10 names of women and men currently living in Germany according to https://www.beliebte-vornamen.de/28071-derzeit-lebende-bevoelkerung.htm
                        elif term in MALE:
                            sentences += [
                                    fill_template(template=template, term=term, role=short_role_masc, gender='MALE')
                                        for template in short_clear_success_template
                            ] #names are top 10 names of women and men currently living in Germany according to https://www.beliebte-vornamen.de/28071-derzeit-lebende-bevoelkerung.htm
                        else:
                            sentences += [
                                    fill_template(template, term, short_role_fem, gender='FEMALE')
                                        for template in adjective_template
                            ]
                            sentences += [
                                    fill_template(template, term, short_role_masc, gender='MALE')
                                        for template in adjective_template
                            ]  
                elif args.test_type == 'medium':
                    if term in FEMALE:
                        sentences += [
                                fill_template(template, term, long_role, gender='FEMALE')
                                    for template in medium_success_template
                        ] #names are top 10 names of women and men currently living in Germany according to https://www.beliebte-vornamen.de/28071-derzeit-lebende-bevoelkerung.htm
                    elif term in MALE:
                        sentences += [
                                fill_template(template, term, long_role, gender='MALE')
                                    for template in medium_success_template
                        ] #names are top 10 names of women and men currently living in Germany according to https://www.beliebte-vornamen.de/28071-derzeit-lebende-bevoelkerung.htm
                    else:
                        sentences += [
                                fill_template(template, term, long_role, gender='FEMALE')
                                    for template in adjective_template
                        ]
                        sentences += [
                                fill_template(template, term, long_role, gender='MALE')
                                    for template in adjective_template
                        ]
                elif args.test_type == 'medium_long':
                    if 'competent' in input_path:
                        if term in FEMALE:
                            sentences += [
                                    fill_template(template=template, term=term, role=long_role, gender='FEMALE')
                                        for template in medium_long_ambig_success_template
                            ] #names are top 10 names of women and men currently living in Germany according to https://www.beliebte-vornamen.de/28071-derzeit-lebende-bevoelkerung.htm
                        elif term in MALE:
                            sentences += [
                                    fill_template(template=template, term=term, role=long_role, gender='MALE')
                                        for template in medium_long_ambig_success_template
                            ] #names are top 10 names of women and men currently living in Germany according to https://www.beliebte-vornamen.de/28071-derzeit-lebende-bevoelkerung.htm
                        else:
                            sentences += [
                                    fill_template(template, term, long_role, gender='FEMALE')
                                        for template in adjective_template
                            ]
                            sentences += [
                                    fill_template(template, term, long_role, gender='MALE')
                                        for template in adjective_template
                            ]
                    elif 'likable' in input_path:
                        if term in FEMALE:
                            sentences += [
                                    fill_template(template=template, term=term, role=long_role, gender='FEMALE')
                                        for template in medium_long_clear_success_template
                            ] #names are top 10 names of women and men currently living in Germany according to https://www.beliebte-vornamen.de/28071-derzeit-lebende-bevoelkerung.htm
                        elif term in MALE:
                            sentences += [
                                    fill_template(template=template, term=term, role=long_role, gender='MALE')
                                        for template in medium_long_clear_success_template
                            ] #names are top 10 names of women and men currently living in Germany according to https://www.beliebte-vornamen.de/28071-derzeit-lebende-bevoelkerung.htm
                        else:
                            sentences += [
                                    fill_template(template, term, long_role, gender='FEMALE')
                                        for template in adjective_template
                            ]
                            sentences += [
                                    fill_template(template, term, long_role, gender='MALE')
                                        for template in adjective_template
                            ]
                elif args.test_type == 'long':
                    if 'competent' in input_path:
                        if term in FEMALE:
                            sentences += [
                                    fill_template(template, term, long_role, gender='FEMALE')
                                        for template in long_ambig_success_template
                            ] #names are top 10 names of women and men currently living in Germany according to https://www.beliebte-vornamen.de/28071-derzeit-lebende-bevoelkerung.htm
                        elif term in MALE:
                            sentences += [
                                    fill_template(template, term, long_role, gender='MALE')
                                        for template in long_ambig_success_template
                            ] #names are top 10 names of women and men currently living in Germany according to https://www.beliebte-vornamen.de/28071-derzeit-lebende-bevoelkerung.htm
                        else:
                            sentences += [
                                    fill_template(template, term, long_role, gender='FEMALE')
                                        for template in adjective_template
                            ]
                            sentences += [
                                    fill_template(template, term, long_role, gender='MALE')
                                        for template in adjective_template
                            ]
                    elif 'likable' in input_path:
                        if term in FEMALE:
                            sentences += [
                                    fill_template(template, term, long_role, gender='FEMALE')
                                        for template in long_clear_success_template
                            ] #names are top 10 names of women and men currently living in Germany according to https://www.beliebte-vornamen.de/28071-derzeit-lebende-bevoelkerung.htm
                        elif term in MALE:
                            sentences += [
                                    fill_template(template, term, long_role, gender='MALE')
                                        for template in long_clear_success_template
                            ] #names are top 10 names of women and men currently living in Germany according to https://www.beliebte-vornamen.de/28071-derzeit-lebende-bevoelkerung.htm
                        else:
                            sentences += [
                                    fill_template(template, term, long_role, gender='FEMALE')
                                        for template in adjective_template
                            ]
                            sentences += [
                                    fill_template(template, term, long_role, gender='MALE')
                                        for template in adjective_template
                            ]
                elif args.test_type == 'basic':
                    if term in MALE or term in FEMALE:
                        sentences += [
                                fill_template(template, term, long_role, gender='FEMALE')
                                    for template in short_basic_person_template
                        ]
                    else:
                        sentences += [
                                fill_template(template, term, long_role, gender='FEMALE')
                                    for template in short_basic_adj_template
                        ]

            logging.info(toc())
            set_dict['examples'] = sentences
            gc.collect()
        
        logging.info('finished creating sentence temps')
        if len(sets['targ1']['examples']) != len(sets['targ2']['examples']):
            logging.info(
                'Truncating targ1, targ2 to have same size (current sizes: {},\
                    {})'.format(
                    len(sets['targ1']['examples']), len(sets['targ2']['examples'])))
            (sets['targ1']['examples'], sets['targ2']['examples']) = truncate_lists(
                sets['targ1']['examples'], sets['targ2']['examples'])

        (dirname, basename) = os.path.split(input_path)

        if args.test_type !='basic':
            if args.test_type == 'long':
                OUTPUT_SUFFIX = '_1-'
            elif args.test_type == 'medium':
                OUTPUT_SUFFIX = '_1'
            elif args.test_type == 'medium_long':
                OUTPUT_SUFFIX = '_1+3-'
            elif args.test_type == 'short':
                OUTPUT_SUFFIX = '_one_sentence'
            else:
                logging.warning('Unknown test type')
            output_path = os.path.join(dirname, (basename[:len(basename) - 15])+ OUTPUT_SUFFIX + '.jsonl')
        else:
            OUTPUT_SUFFIX = '_one_word'
            output_path = os.path.join(dirname, 'sent-'+(basename[:len(basename) - 15])+ OUTPUT_SUFFIX + '.jsonl')
            
        logging.info('Writing sentence-level test to {}'.format(output_path))
        with open(output_path, 'w', encoding='utf8') as f:
            json.dump(sets, f, indent=2, ensure_ascii=False)
        

if __name__ == '__main__':
    main()
