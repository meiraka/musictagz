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
                        const=('music', 'yaml'),
                        dest='command')
    parser.add_argument('-l', '--load', action='store_const',
                        const=('yaml', 'music'),
                        dest='command')
    parser.add_argument('-r', '-n', '--rewrite', '--dryrun', '--filter',
                        action='store_const',
                        const=('yaml', 'yaml'),
                        dest='command')
    ret = parser.parse_args(argv)
    if ret.command is None:
        ret.command = ('yaml', 'music')
    read, write = ret.command

    data = (read_from_yaml_file(sys.stdin) if read == 'yaml'
            else read_from_music_file('./*'))
    return (write_to_yaml_file(sys.stdout, data) if write == 'yaml'
            else write_to_music_file(data))


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
    return 0


def write_to_music_file(data):
    """Write music deflatten data to music files."""
    flatten_data = tags.flatten(data)
    tags.write(flatten_data)
    return 0
