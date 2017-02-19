"""MusicTagz command line interface."""
# coding: utf-8


import argparse
import sys

import yaml

from musictagz import tags
from musictagz.filter import keys, template, web


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-d', '--dump', action='store_const',
                       const=('music', 'yaml'),
                       dest='command',
                       help='read audio meta data and write yaml to stdout')
    group.add_argument('-l', '--load', action='store_const',
                       const=('yaml', 'music'),
                       dest='command',
                       help='read yaml from stdin and write audio meta data')
    group.add_argument('-f', '-n', '--dryrun', '--filter',
                       action='store_const',
                       const=('yaml', 'yaml'),
                       dest='command',
                       help='read yaml from stdin and write yaml to stdout')

    keys_filter = parser.add_mutually_exclusive_group()
    keys_filter.add_argument('-K', '--keys_upper',
                             action='store_const',
                             const='upper',
                             dest='keys',
                             help='output upppercased key meta data')
    keys_filter.add_argument('-k', '--keys_lower',
                             action='store_const',
                             const='lower',
                             dest='keys',
                             help='output lowercaed key meta data')

    parser.add_argument('--template',
                        action='store_const',
                        const=True,
                        dest='template',
                        help='add template key/value')

    parser.add_argument('--touhouwiki',
                        nargs=1,
                        action='store',
                        dest='touhouwiki',
                        default='',
                        help='use touhouwiki as meta data')

    ret = parser.parse_args(argv)
    if ret.command is None:
        ret.command = ('yaml', 'music')
    read, write = ret.command

    data = (read_from_yaml_file(sys.stdin) if read == 'yaml'
            else read_from_music_file('./*'))
    if ret.template:
        data = tags.deflatten(template.musicbrainz(tags.flatten(data)))
    if ret.touhouwiki:
        data = tags.deflatten(web.touhouwiki(ret.touhouwiki[0], tags.flatten(data)))
    if ret.keys == 'upper':
        data = keys.upper(data)
    elif ret.keys == 'lower':
        data = keys.lower(data)
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
