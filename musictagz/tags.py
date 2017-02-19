"""Read/Write music data and audio files."""

import glob
import os
from musictagz.codecs import auto, error


GLOBBING_MIN_LEN = 2


def flatten(data):
    """Generate music data per songs."""
    ret = {}
    for globpath, type_kv in data.iteritems():
        files = [globpath] if os.path.exists(globpath) else glob.glob(globpath)
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
    lname = globbing_lname(data)
    rname = globbing_rname(data, lname)
    cname = globbing_cname(data, lname, rname)
    if cname:
        return u'*'.join([lname, cname, rname])
    else:
        return u'*'.join([lname, rname])


def globbing_lname(data):
    pathlist = data.keys()
    base = pathlist[0]
    for n in xrange(99, GLOBBING_MIN_LEN - 1, -1):
        searchword = base[:n].strip()
        if all(searchword in path for path in pathlist):
            return searchword
    return u''


def globbing_rname(data, lname):
    lsize = len(lname)
    pathlist = [i[lsize:] for i in data.keys()]
    base = pathlist[0]
    for n in xrange(99, GLOBBING_MIN_LEN - 1, -1):
        searchword = base[-n:].strip()
        if all(searchword in path for path in pathlist):
            return searchword
    return u''


def globbing_cname(data, lname, rname):
    lsize = len(lname)
    rsize = len(rname)
    pathlist = [i[lsize:][:rsize] for i in data.keys()]
    base = pathlist[0]
    base_len = len(base)
    for n in xrange(99, GLOBBING_MIN_LEN - 1, -1):
        pad = 0
        found = False
        while pad + n <= base_len:
            searchword = base[pad:pad+n].strip()
            found = all(searchword in path for path in pathlist)
            if found:
                return searchword
            pad += 1
    return u''
