"""Read/Write music data and audio files."""


import glob
from musictagz.codecs import auto, error


def flatten(data):
    """Generate music data per songs."""
    ret = {}
    for path, type_kv in data.iteritems():
        files = glob.glob(path)
        for type_, kv in type_kv.iteritems():
            for key, value in kv.iteritems():
                for filepath in files:
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
