"""MusicTagz command line interface."""


import argparse
import sys

import yaml

from musictagz import tags


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dump', action='store_const',
                        const='dump',
                        dest='command')
    parser.add_argument('-l', '--load', action='store_const',
                        const='load',
                        dest='command')
    parser.add_argument('-r', '--rewrite', action='store_const',
                        const='rewrite',
                        dest='command')
    ret = parser.parse_args(argv)
    if ret.command == 'dump':
        dump_yaml('./*')
        return 0
    elif ret.command == 'rewrite':
        rewrite()
        return 0
    else:
        load_yaml()
        return 0


def read_from_yaml_file(f):
    """Return flatten music data from musictagz yaml file."""
    data = yaml.safe_load(f.read())

    def u(s):
        if type(s) == str:
            return unicode(s)
        elif type(s) == dict:
            return dict([(u(k), u(v)) for k, v in s.iteritems()])
        elif type(s) == list:
            return [u(i) for i in s]
        else:
            return s

    return u(data)


def read_from_music_file(glob_path):
    """Return flatten music data from music files."""
    flatten_data = tags.read(glob_path)
    return tags.deflatten(flatten_data)


def write_to_yaml_file(f, data):
    """Write musictagz yaml format to file from deflatten data."""
    out = yaml.safe_dump(data, default_flow_style=False,
                         allow_unicode=True, encoding='utf8')
    f.write(out)


def write_to_music_file(data):
    """Write music deflatten data to music files."""
    flatten_data = tags.flatten(data)
    tags.write(flatten_data)


def dump_yaml(glob_path):
    data = read_from_music_file(glob_path)
    write_to_yaml_file(sys.stdout, data)
    return 0


def load_yaml():
    data = read_from_yaml_file(sys.stdin)
    write_to_music_file(data)
    return 0


def rewrite():
    data = read_from_yaml_file(sys.stdin)
    write_to_yaml_file(sys.stdout, data)
    return 0
