"""Flac music tag reader/writer."""


import subprocess

from musictagz import tagtype


def checktype(path):
    """Check path is flac file."""
    cmd = ['file', path.encode('utf-8')]
    return 'FLAC' in subprocess.check_output(cmd).decode('utf-8')


def read(path):
    """Read flac tag."""
    tag = {}
    cmd = ['metaflac', '--no-utf8-convert',
           '--export-tags-to=-', path.encode('utf-8')]
    output = subprocess.check_output(cmd).decode('utf-8')
    plaintag = tag.setdefault(tagtype.PLAIN, {})
    lastkey = ''
    for line in output.splitlines():
        if u'=' in line:
            key, value = line.split(u'=', 1)
            lastkey = key
            if key not in plaintag:
                plaintag[key] = value
            elif type(plaintag[key]) == list:
                plaintag[key].append(value)
            else:
                plaintag[key] = [plaintag[key], value]
        else:
            value = plaintag[lastkey]
            if type(value) == list:
                value[-1] = u'\n'.join([value[-1], line])
                plaintag[lastkey] = value
            else:
                value = u'\n'.join([value, line])
                plaintag[lastkey] = value
    return tag


def write(path, tag):
    """Write flac tag."""
    cmd = ['metaflac',
           '--remove-all-tags', path.encode('utf-8')]
    subprocess.check_call(cmd)

    # use import-tags-from
    singleline_values = []
    for k, v in tag[tagtype.PLAIN].iteritems():
        k = k.encode('utf-8')
        if type(v) == list:
            for vpart in v:
                vpart = vpart.encode('utf-8')
                cmd = ['metaflac', '--no-utf8-convert',
                       '--set-tag={}={}'.format(k, vpart), path]
                if '\n' not in k and '\n' not in vpart:
                    singleline_values.append('{}={}'.format(k, vpart))
                else:
                    subprocess.check_call(cmd)
        else:
            v = v.encode('utf8')
            cmd = ['metaflac', '--no-utf8-convert',
                   '--set-tag={}={}'.format(k, v), path]
            if '\n' not in k and '\n' not in v:
                singleline_values.append('{}={}'.format(k, v))
            else:
                subprocess.check_call(cmd)

    proc = subprocess.Popen(['metaflac', '--no-utf8-convert',
                             '--import-tags-from=-', path],
                            stdin=subprocess.PIPE)
    proc.communicate('\n'.join(singleline_values) + '\n')
    proc.wait()
