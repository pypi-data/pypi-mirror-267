# uncategorized functions

import pickle, re, os, json, sys


cwd_template = '''#!/usr/bin/python3
import os,sys

script_path = os.path.realpath(__file__)
script_dir = os.path.dirname(script_path)'''

import __main__
script_path = os.path.realpath(__main__.__file__)
script_dir = os.path.dirname(script_path)

def match_in_file(pat, path):
    return re.findall(pat, read_file(path), re.MULTILINE)

def load_obj(path):
    with open(path, "rb") as f:
        return pickle.load(f)

def load_json(path):
    with open(path, "rb") as f:
        return json.load(f)

def dump_obj(path, data):
    with open(path, "wb") as f:
        pickle.dump(data, f)

def write_file(path, content):
    with open(path, 'w') as f:
        f.write(content)

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

def dump_json(path, obj, indent=2):
    with open(path, 'w') as f:
        json.dump(obj, f, indent=indent, cls=SetEncoder)

def read_file(path):
    with open(path, 'r') as f:
        return f.read()

def read_file_bytes(path):
    with open(path, 'rb') as f:
        return f.read()

def load_py_file(path):
    with open(path, 'r') as f:
        return eval(f.read())

def match_in_str(pat, s):
    import re
    return re.findall(pat, s, re.MULTILINE)

def match_in_file(pat, path):
    import re
    return re.findall(pat, read_file(path), re.MULTILINE)

def match_in_file_bytes(pat, path):
    import re
    return re.findall(pat, read_file_bytes(path), re.MULTILINE)

def random_sample_dict(d, count):
    import random
    out = {}
    for i in random.sample(list(d), count):
        out[i] = d[i]
    return out

## ======= other ==========

def average(lst):
    return sum(lst) / len(lst)

def listdir(dataset):
    dataset = dataset.removesuffix('/')
    return [dataset+'/'+i for i in os.listdir(dataset)]

from pprint import PrettyPrinter

class NoStringWrappingPrettyPrinter(PrettyPrinter):
    def _format(self, object, *args):
        if isinstance(object, str):
            width = self._width
            self._width = sys.maxsize
            try:
                super()._format(object, *args)
            finally:
                self._width = width
        else:
            super()._format(object, *args)

def pprint_obj(path, obj):
    with open(path, 'w') as f:
        f.write(NoStringWrappingPrettyPrinter().pformat(obj))
