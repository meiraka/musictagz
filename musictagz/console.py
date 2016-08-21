"""MusicTagz command line interface."""


from __future__ import print_function
import argparse
import sys

import yaml

from musictagz import tags

DEFAULT_PATH = './tracks.yml'


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dump', action='store_true', dest='dump')
    parser.add_argument('-l', '--load', action='store_false', dest='dump')
    ret = parser.parse_args(argv)
    if ret.dump:
        dump_yaml('./*', DEFAULT_PATH)
        return 0
    else:
        load_yaml(DEFAULT_PATH)
        return 0


def dump_yaml(glob_path, yaml_path):
    data = tags.read(glob_path)
    out = yaml.safe_dump(data, default_flow_style=False,
                         allow_unicode=True, encoding='utf8')
    with open(yaml_path, 'w') as f:
        f.write(out)


def load_yaml(yaml_path):
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f.read())
    flatten_data = tags.flatten(data)
    tags.write(flatten_data)
