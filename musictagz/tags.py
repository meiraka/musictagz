"""Read/Write music data and audio files."""

import glob
import os
from musictagz.codecs import auto, error


def flatten(data):
    """Generate music data per songs."""
    ret = {}
    for globpath, type_kv in data.iteritems():
        files = glob.glob(globpath)
        for type_, kv in type_kv.iteritems():
            for key, value in kv.iteritems():
                for filepath in files:
                    filepath = os.path.normpath(filepath)
                    music = ret.setdefault(filepath, {})
                    music.setdefault(type_, {})[key] = value
    return ret


def write(flatten_data):
    """Write flatten output to files."""
    for path, tag in flatten_data.iteritems():
        try:
            auto.write(path, tag)
        except error.UnsupportedCodecError:
            pass


def read(glob_path):
    """Read tag from files."""
    ret = {}
    for path in glob.glob(glob_path):
        try:
            ret[path] = auto.read(path)
        except error.UnsupportedCodecError:
            pass
    return ret


def deflatten(flatten_data):
    """Globbing flatten_data."""
    ret = {}
    same_key_value = search_same_key_value(flatten_data)
    ret[globbing_path(flatten_data)] = same_key_value
    # remove same key value
    for path, type_kv in flatten_data.iteritems():
        for type_, kv in type_kv.iteritems():
            if type_ not in same_key_value:
                ret.setdefault(path, {})[type_] = kv
                continue
            for key, value in kv.iteritems():
                if key not in same_key_value[type_]:
                    ret.setdefault(path, {}).setdefault(type_, {})[key] = value
    return ret


def search_same_key_value(data):
    old_kv = {}
    for index, (path, type_kv) in enumerate(data.iteritems()):
        if index == 0:
            old_kv = type_kv
            continue
        new_kv = {}
        for type_, kv in type_kv.iteritems():
            for key, value in kv.iteritems():
                try:
                    if old_kv[type_][key] == value:
                        new_kv.setdefault(type_, {})[key] = value
                except KeyError:
                    pass
        old_kv = new_kv
    return old_kv


def globbing_path(data):
    pathlist = data.keys()
    base = pathlist[0]
    base_len = len(base)
    globstr = None
    for n in xrange(1, 100):
        pad = 0
        found = False
        while pad + n <= base_len:
            searchword = base[pad:pad+n]
            found = all(searchword in path for path in pathlist)
            if found:
                if pad == 0:
                    globstr = '{}*'.format(searchword)
                    break
                elif pad + n < base_len:
                    globstr = '*{}*'.format(searchword)
                else:
                    globstr = '*{}'.format(searchword)
            pad += 1
        if not found:
            break
    if globstr is not None:
        return globstr
