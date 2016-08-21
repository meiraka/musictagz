"""Flac music tag reader/writer."""


import subprocess

from musictagz import tagtype


def checktype(path):
    """Check path is flac file."""
    cmd = ['file', path]
    return 'FLAC' in subprocess.check_output(cmd).decode('utf-8')


def read(path):
    """Read flac tag."""
    tag = {}
    cmd = ['metaflac', '--no-utf8-convert',
           '--export-tags-to=-', path]
    output = subprocess.check_output(cmd).decode('utf-8')
    plaintag = tag.setdefault(tagtype.PLAIN, {})
    for line in output.splitlines():
        key, value = line.split('=', 1)
        if key not in plaintag:
            plaintag[key] = value
        elif type(plaintag[key]) == list:
            plaintag[key].append(value)
        else:
            plaintag[key] = [plaintag[key], value]
    return tag


def write(path, tag):
    """Write flac tag."""
    cmd = ['metaflac',
           '--remove-all-tags', path]
    subprocess.check_call(cmd)
    for k, v in tag[tagtype.PLAIN].iteritems():
        k = k.encode('utf-8')
        if type(v) == list:
            for vpart in v:
                vpart = vpart.encode('utf-8')
                cmd = ['metaflac', '--no-utf8-convert',
                       '--set-tag={}={}'.format(k, vpart), path]
                subprocess.check_call(cmd)
        else:
            v = v.encode('utf8')
            cmd = ['metaflac', '--no-utf8-convert',
                   '--set-tag={}={}'.format(k, v), path]
            subprocess.check_call(cmd)
