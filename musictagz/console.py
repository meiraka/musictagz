"""MusicTagz command line interface."""


import argparse
import sys

import yaml

from musictagz import tags


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dump', action='store_true', dest='dump')
    parser.add_argument('-l', '--load', action='store_false', dest='dump')
    ret = parser.parse_args(argv)
    if ret.dump:
        dump_yaml('./*')
        return 0
    else:
        load_yaml()
        return 0


def dump_yaml(glob_path):
    flatten_data = tags.read(glob_path)
    data = tags.deflatten(flatten_data)
    out = yaml.safe_dump(data, default_flow_style=False,
                         allow_unicode=True, encoding='utf8')
    sys.stdout.write(out)
    return 0


def load_yaml():
    data = yaml.safe_load(sys.stdin.read())

    def u(s):
        if type(s) == str:
            return unicode(s)
        elif type(s) == dict:
            return dict([(u(k), u(v)) for k, v in s.iteritems()])
        elif type(s) == list:
            return [u(i) for i in s]
        else:
            return s

    data = u(data)

    flatten_data = tags.flatten(data)
    tags.write(flatten_data)
    return 0
