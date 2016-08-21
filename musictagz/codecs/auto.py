"""Auto detect codec."""

from musictagz.codecs import flac
from musictagz.codecs import error


def detect(path):
    """Return given file type codec tag editor."""
    if flac.checktype(path):
        return flac
    else:
        raise error.UnsupportedCodecError()


def read(path):
    """Read audio file tag."""
    return detect(path).read(path)


def write(path, tag):
    """Write audio file tag."""
    return detect(path).write(path, tag)
