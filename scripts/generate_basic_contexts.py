#!/usr/bin/env python3
# has to be run from scripts dir

import logging
import json
import os
import re
import random
from german_nouns.lookup import Nouns
from ttictoc import tic,toc
from genderdeterminator import GenderDeterminator
import Levenshtein
import csv
import gc

PERSON_RE = re.compile(
    r'\b(?:Frau|Mann|Mädchen|Junge|Schwester|Bruder|Tochter|Sohn|'
    r'Mutter|Vater|Tante|Onkel|Großmutter|Großvater|Amerikaner)\b')

OUTPUT_PREFIX = 'sent-'
ADJECTIVES = {
    'loyal',
    'ehrlich',
    'sanft',
    'glücklich',
    'fröhlich',
    'hässlich',
    'verfault',
    'weich',
    'leise',
    'kompromittierend',
    'rational',
    'ruhig',
    'liebenswürdig',
    'gefällig',
    'unterwürfig',
    'annehmlich',
    'vorsichtig',
    'freundlich',
    'unterstützend',
    'nett',
    'mild',
    'zurückhaltend',
    'passiv',
    'gleichgültig',
    'devot',
    'schrill',
    'laut',
    'streitlustig',
    'irrational',
    'wütend',
    'missbräuchlich',
    'unausstehlich',
    'beherrschend',
    'nörgelnd',
    'dreist',
    'feindselig',
    'entmannend',
    'gemein',
    'harsch',
    'keck',
    'aggressiv',
    'eigensinnig',
    'tyrannisch',
    'wundervoll',
    'schrecklich',
    'grauenhaft',
    'gehässig',
    'fürchterlich',
    'professionell',
    'böse',
    'hoffnungslos',
    'traurig',
    'düster',
    'weinerlich',
    'miserabel',
    'depressiv',
    'krank',
    'unbeständig',
    'labil',
    'wechselhaft',
    'flüchtig',
    'kurzfristig',
    'kurz',
    'gelegentlich',
    'dauerhaft',
    'konstant',
    'beharrlich',
    'chronisch',
    'anhaltend',
    'kompetent',
    'produktiv',
    'effektiv',
    'ambitioniert',
    'aktiv',
    'bestimmt',
    'stark',
    'hartnäckig',
    'mutig',
    'durchsetzungsfähig',
    'inkompetent',
    'unproduktiv',
    'ineffektiv',
    'unambitioniert',
    'passiv',
    'unentschlossen',
    'schwach',
    'sanft',
    'schüchtern',
    'unsicher',
    'angenehm',
    'fair',
    'ehrlich',
    'vertrauenswürdig',
    'selbstlos',
    'entgegenkommend',
    'sympathisch',
    'beliebt',
    'grob',
    'hinterhältig',
    'manipulativ',
    'unehrlich',
    'egoistisch',
    'aufdringlich',
    'unsympathisch',
    'unbeliebt',
    'weiblich',
    'männlich'
}

MASS_NOUNS = {
    'Freiheit',
    'Gesundheit',
    'Liebe',
    'Frieden',
    'Jubel',
    'Loyalität',
    'Dreck',
    'Trauer',
    'Hass',
    'Armut',
    'Leid',
    'Dynamit',
    'Tränengas',
    'Physik',
    'Analysis',
    'Wissenschaft',
    'Chemie',
    'Astronomie',
    'NASA',
    'Poesie',
    'Kunst',
    'Literatur',
    'Mathe',
    'Algebra',
    'Geometrie',
    'immer',
    'ewig'
    'Erbrochenes',
    "Dichtkunst",
    "Einstein",
    "Shakespeare",
    "Berechnungen",
    "Gelächter"
}

PLURAL_NOUNS = {
    'Eltern',
    'Kinder',
    'Cousins',
    'Verwandten',
    'Nummern',
    'Gleichungen',
    "Zahlen",
}

NOUNS_OTHER = {
     "Aster",
      "Klee",
      "Hyacinthe",
      "Ringelblume",
      "Mohn",
      "Rhododendron",
      "Krokus",
      "Schwertlilie",
      "Orchidee",
      "Rose",
      "Hasenglöckchen",
      "Osterglocke",
      "Flieder",
      "Stiefmütterchen",
      "Tulpe",
      "Butterblume",
      "Gänseblümchen",
      "Lilie",
      "Pfingstrose",
      "Veilchen",
      "Nelke",
      "Gladiole",
      "Magnolie",
      "Petunie",
      "Zinnie",
      "Ameise",
      "Raupe",
      "Floh",
      "Grashüpfer",
      "Spinne",
      "Bettwanze",
      "Tausendfüßer",
      "Fliege",
      "Made",
      "Vogelspinne",
      "Biene",
      "Kakerlake",
      "Mücke",
      "Moskito",
      "Termite",
      "Käfer",
      "Grille",
      "Hornisse",
      "Motte",
      "Wespe",
      "Kriebelmücke",
      "Libelle",
      "Pferdebremse",
      "Kakerlake",
      "Rüsselkäfer"
      "Freund",
      "Himmel",
      "Genuss",
      "Diamant",
      "Regenbogen",
      "Diplom",
      "Geschenk",
      "Ehre",
      "Wunder",
      "Sonnenaufgang",
      "Familie",
      "Paradies",
      "Urlaub",
      "Missbrauch",
      "Absturz",
      "Mord",
      "Krankheit",
      "Unfall",
      "Tod",
      "Gift",
      "Übergriff",
      "Disaster",
      "Tragödie",
      "Scheidung",
      "Gefängnis",
      "Krebserkrankung",
      'Freude',
      'Zärtlichkeit',
      'Führungskraft',
      'Management',
      "Unternehmen",
      "Gehalt",
      "Büro",
      "Geschäft",
      "Karriere",
      "Haus",
      "Hochzeit",
      "Addition",
      "Tanz",
      "Roman",
      "Symphonie",
      "Schauspiel",
      "Skulptur",
      "Technologie",
      "Experiment",
      "Ehe"
}

VERBS = {
    'verschmutzen',
    'töten',
    'stinken',
}

NAME_TEMPLATES = (
    'Dies ist {term}.',
    'Das ist {term}.',
    'Da ist {term}.',
    'Hier ist {term}.',
    '{term} ist hier.',
    '{term} ist da.',
    '{term} ist eine Person.',
    'Der Name dieser Person ist {term}.',
)

SUBJECT_PRONOUN_TEMPLATES = (
    '{term} ist hier.',
    '{term} ist da.',
    'Hier ist {term}.',
    'Da ist {term}.',
    '{term} ist eine Person.',
)

OBJECT_PRONOUN_TEMPLATES = (
    'Es gehört {term}.',
    'Das gehört {term}.',
    '{term} gehört das.',
)

POSSESSIVE_PRONOUN_TEMPLATES = (
    'Es ist {term}.',
    'Das ist {term}.',
    'Dort ist {term}.',
    'Hier ist {term}.',
    'Es ist {term}.',
    '{term} ist da.',
    '{term} ist hier.',
)

ADJECTIVE_TEMPLATES = (
    'Es ist {term}.',
    'Das ist {term}.',
    'Sie sind {term}.',
)

MASS_NOUN_TEMPLATES = (
    'Dies ist {term}.',
    'Das ist {term}.',
    'Dort ist {term}.',
    'Es ist {term}.',
)

VERB_TEMPLATES = (
    'Es wird {term}.',
    'Es hat {term}.',
    'Es kann {term}.',
    'Es könnte {term}.',
    'Das wird {term}.',
    'Das hat {term}.',
    'Das kann {term}.',
    'Das könnte {term}.',
)

SINGULAR_NOUN_TEMPLATES = (
    'Es ist {article} {term}.',
    'Das ist {article} {term}.',
    'Da ist {article} {term}.',
    'Hier ist {article} {term}.',
    '{article_definite} {term} ist hier.',
    '{article_definite} {term} ist da.',
)

PLURAL_NOUN_TEMPLATES = (
    'Dies sind {term}.',
    'Es sind {term}.',
    'Sie sind {term}.',
    'Die {term} sind hier.',
    'Die {term} sind dort.',
)

SINGULAR_PERSON_TEMPLATES = (
    '{article} {term} ist eine Person.',
)

PLURAL_PERSON_TEMPLATES = (
    '{term} sind Leute.',
)

SINGULAR_THING_TEMPLATES = (
    '{article} {term} ist ein Ding.',
    'Es ist {article} {term}.',
)

PLURAL_THING_TEMPLATES = (
    '{term} sind Dinge.',
)

unknown_noun = []

def fill_template(template, term, counter_verwandt=0):
    nouns = Nouns()
    gd = GenderDeterminator()
    try:
        if gd.get_gender(term) == 'f':
            article = 'eine'
            article_definite = 'die'
            term=term
        elif gd.get_gender(term) == 'm':
            article = 'ein'
            article_definite = 'der'
            term=term
        else:
            article = 'ein'
            article_definite = 'das'
            term=term
    except:
        try:
            if nouns[term][0].get('genus') == 'f':
                article = 'eine'
                article_definite = 'die'
                term=term
            elif nouns[term][0].get('genus') == 'm':
                article = 'ein'
                article_definite = 'der'
                term=term
            else:
                article = 'ein'
                article_definite = 'das'
                term=term
        except:
            article = 'ein'
            article_definite = 'der'
            term=term
            if term in MASS_NOUNS or term in PLURAL_NOUNS or \
                term in NOUNS_OTHER:
                logging.warning(f"{term} is not in german-nouns. Articles 'ein' \
                     and 'der' will be used.")
                unknown_noun.append(term)
    if term =='Verwandte':
        if counter_verwandt==0:
            article = 'eine'
            article_definite = 'die'
            term=term
            sentence = template.format(article=article, article_definite=article_definite, \
                term=term)
        elif counter_verwandt==1:
            article = 'ein'
            article_definite = 'der'
            if '{article_definite}' in template:
                term=term
            else:
                term=term+'r'
            sentence = template.format(article=article, article_definite=article_definite, \
                term=term)
    elif term=='Verwandten':
        article = 'eine'
        article_definite = 'die'
        if 'Die' in template:
            term=term
        else:
            term=term[:-1]
        sentence = template.format(article=article, article_definite=article_definite, \
            term=term)
    else:
        sentence = template.format(article=article, article_definite=article_definite, \
            term=term)
    return sentence[0].upper() + sentence[1:]


def singularize(s):
    nouns = Nouns()
    singular = nouns[s][0].get('flexion').get('akkusativ singular')
    if singular == None:
        singular = nouns[s][0].get('flexion').get('akkusativ singular gemischt')
    return singular

def pluralize(s, case=True): # customized from https://github.com/jarinox/python-grammar-de/blob/master/gmrde/woerterbuch.py
    dict_path="data/german.csv" # from https://github.com/jarinox/python-grammar-de
    dict_csv = open(dict_path, "r")
    re = csv.reader(dict_csv)
    dict_de = list(re)
    sLower = s.lower()
    sReplaceSS = s.replace('ss', 'ß')
    sLowerReplaceSS = sReplaceSS.lower()
    treffer = []
    for item in dict_de:
        # get words similar to s
        if(case):
            if(((Levenshtein.ratio(item[1], s) > 0.95) or \
                (Levenshtein.ratio(item[1], sReplaceSS) > 0.95)) and \
                "PLU" in item[2] and "SUB" in item[2] and "AKK" in item[2]):
                treffer.append(item)
        else:
            if(((Levenshtein.ratio(item[1].lower(), sLower) > 0.95) or \
                (Levenshtein.ratio(item[1], sLowerReplaceSS) > 0.95)) and \
                "PLU" in item[2] and "SUB" in item[2] and "AKK" in item[2]):
                treffer.append(item)
    
    # no results sets treffer to false
    if(treffer == []):
        if(treffer == []):    
            treffer = False
    
    # filter results if there are multiple possibilites
    if(isinstance(treffer, list) and len(treffer)> 1):
        treffer_reduced = treffer
        del treffer_reduced[1:len(treffer_reduced)+1]

        # returned value should not be empty   
        if (len(treffer_reduced)==0):
            treffer = treffer[0][0]
        else:
            treffer=treffer_reduced[0][0]
    elif isinstance(treffer, bool):
        nouns = Nouns()
        try:
            treffer = nouns[s.capitalize()][0].get('flexion').get('akkusativ plural')
        except:
            logging.warning(f'no known plural of {s}')
        if treffer == None:
            logging.warning(f'no known plural of {s}')
            unknown_noun.append(s)
            treffer=s
        if isinstance(treffer, bool):
            treffer=s
    else:
        treffer = treffer[0][0]
    if s == "Führungskraft":
        treffer = "Führungskräfte"
    if s == "Gehalt":
        treffer = "Gehälter"
    gc.collect()
    return treffer

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
                        help='Paths to word-level json test files.  Output '
                             'files will be named by prepending {} to each '
                             'input filename.'.format(OUTPUT_PREFIX))
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
                if term[0].isupper() and not term in MASS_NOUNS and not term in PLURAL_NOUNS and \
                        not term in NOUNS_OTHER and PERSON_RE.search(term) is None:
                        logging.info(f'{term} is a name.')
                        sentences += [
                            fill_template(template, term)
                            for template in NAME_TEMPLATES
                        ] #names are top 10 names of women and men currently living in Germany according to https://www.beliebte-vornamen.de/28071-derzeit-lebende-bevoelkerung.htm
                elif term in ADJECTIVES:
                    logging.info(f'{term} is an adjective.')
                    tic()
                    sentences += [
                        fill_template(template, term)
                        for template in ADJECTIVE_TEMPLATES
                    ]
                    logging.info(toc())
                elif term in VERBS:
                    logging.info(f'{term} is a verb.')
                    for template in VERB_TEMPLATES:
                        if ' hat ' in template:
                            if term=="verschmutzen":
                                term="verschmutzt"
                            elif term=="töten":
                                term="getötet"
                            elif term=="stinken":
                                term="gestunken"
                            else:
                                term=term
                        else:
                            logging.warning(f'{term} not covered in verb conjugation ')
                        tic()    
                        sentences += [
                            fill_template(template, term)
                        ]
                        logging.info(toc())
                elif term in MASS_NOUNS:
                    logging.info(f'{term} is a mass-noun.')
                    tic()
                    sentences += [
                        fill_template(template, term)
                        for template in MASS_NOUN_TEMPLATES
                    ]
                    logging.info(toc())
                elif term in ('er', 'sie'):
                    logging.info(f'{term} in subject-pronoun.')
                    tic()
                    sentences += [
                        fill_template(template, term)
                        for template in SUBJECT_PRONOUN_TEMPLATES
                    ]
                    logging.info(toc())
                elif term in ('ihm', 'ihr'):
                    logging.info(f'{term} in object-pronoun.')
                    tic()
                    sentences += [
                        fill_template(template, term)
                        for template in OBJECT_PRONOUN_TEMPLATES
                    ]
                    logging.info(toc())
                elif term in ('seins', 'ihrs'):
                    logging.info(f'{term} in possessive_pronoun.')
                    tic()
                    sentences += [
                        fill_template(template, term)
                        for template in POSSESSIVE_PRONOUN_TEMPLATES
                    ]
                    logging.info(toc())
                else:
                    if term in PLURAL_NOUNS:
                        logging.info(f'{term} is a plural noun.')
                        if term == 'Eltern':
                            singular_term='Elternteil'
                        else:
                            singular_term = singularize(term)
                        plural_term = term
                    else:
                        logging.info(f'{term} is a thing.')
                        singular_term = term
                        plural_term = pluralize(term)
                    
                    tic()
                    sentences += [
                        fill_template(template, singular_term, 0)
                        for template in SINGULAR_NOUN_TEMPLATES
                    ]
                    logging.info(toc())
                    tic()
                    if term.startswith("Verwandt"):
                        sentences += [
                            fill_template(template, singular_term, 1)
                            for template in SINGULAR_NOUN_TEMPLATES
                        ]
                    logging.info(toc())
                    
                    tic()
                    sentences += [
                        fill_template(template, plural_term)
                        for template in PLURAL_NOUN_TEMPLATES
                    ]
                    logging.info(toc())

                    if PERSON_RE.search(term) is not None:
                        tic()
                        sentences += [
                            fill_template(template, singular_term)
                            for template in SINGULAR_PERSON_TEMPLATES
                        ]
                        logging.info(toc())

                        tic()
                        sentences += [
                            fill_template(template, plural_term)
                            for template in PLURAL_PERSON_TEMPLATES
                        ]
                        logging.info(toc())
                    elif term not in ['Eltern', 'Kinder', 'Cousins', 'Verwandten']:
                        tic()
                        sentences += [
                            fill_template(template, plural_term)
                            for template in PLURAL_THING_TEMPLATES
                        ]
                        logging.info(toc())
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
        output_path = os.path.join(dirname, OUTPUT_PREFIX + basename)

        logging.info('Writing sentence-level test to {}'.format(output_path))
        with open(output_path, 'w', encoding='utf8') as f:
            json.dump(sets, f, indent=2, ensure_ascii=False)
        
        logging.warning('Nouns with inaccurate plurals:\n{}'.format(unknown_noun))


if __name__ == '__main__':
    main()
