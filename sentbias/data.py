''' Helper functions related to loading and saving data '''
import json
import h5py
import logging as log

WEAT_SETS = ["targ1", "targ2", "attr1", "attr2"]
CATEGORY = "category"


def load_json(sent_file):
    ''' Load from json. We expect a certain format later, so do some post processing '''
    log.info("Loading %s..." % sent_file)
    all_data = json.load(open(sent_file, 'r'))
    data = {}
    for k, v in all_data.items():
        examples = v["examples"]
        data[k] = examples
        v["examples"] = examples
    return all_data  # data


def load_encodings(enc_file):
    ''' Load cached vectors from a model. '''
    encs = dict()
    with h5py.File(enc_file, 'r') as enc_fh:
        for split_name, split in enc_fh.items():
            split_d, split_exs = {}, {}
            for ex, enc in split.items():
                if ex == CATEGORY:
                    split_d[ex] = enc.value
                else:
                    split_exs[ex] = enc[:]
            split_d["encs"] = split_exs
            encs[split_name] = split_d
    return encs


def save_encodings(encodings, enc_file):
    ''' Save encodings to file '''
    with h5py.File(enc_file, 'w') as enc_fh:
        for split_name, split_d in encodings.items():
            split = enc_fh.create_group(split_name)
            split[CATEGORY] = split_d["category"]
            for ex, enc in split_d["encs"].items():
                split[ex] = enc
