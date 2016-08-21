import subprocess

from musictagz.codecs import flac
from musictagz import tagtype


def test_checktype_return_true_if_flac(monkeypatch):
    def mock_check_output(args):
        assert ['file', '01.flac'] == args
        return ('01.flac: FLAC audio bitstream data, '
                '16 bit, stereo, 44.1 kHz, 9781380 samples')

    monkeypatch.setattr(subprocess, 'check_output', mock_check_output)
    assert flac.checktype('01.flac')


def test_checktype_return_false_if_not_flac(monkeypatch):
    def mock_check_output(args):
        assert ['file', '01.ogg'] == args
        return ('01.ogg: Ogg data, Vorbis audio, stereo, '
                '44100 Hz, ~160000 bps, created by: Xiph.Org libVorbis I')

    monkeypatch.setattr(subprocess, 'check_output', mock_check_output)
    assert False == flac.checktype('01.ogg')


def test_read(monkeypatch):
    def mock_check_output(args):
        assert ['metaflac', '--no-utf8-convert',
                '--export-tags-to=-', '01.flac'] == args
        return '''ALBUM=foo
ALBUMARTIST=bar
TITLE=baz
ARTIST=qux
ARTISTS=q
ARTISTS=u
ARTISTS=x
'''
    monkeypatch.setattr(subprocess, 'check_output', mock_check_output)
    expect = {
        tagtype.PLAIN:
            {'ALBUM': 'foo',
             'ALBUMARTIST': 'bar',
             'TITLE': 'baz',
             'ARTIST': 'qux',
             'ARTISTS': ['q', 'u', 'x']}}
    assert expect == flac.read('01.flac')


def test_write(monkeypatch):
    path = '01.flac'
    tag = {
        tagtype.PLAIN:
            {'ALBUM': 'foo',
             'ALBUMARTIST': 'bar',
             'TITLE': 'baz',
             'ARTIST': 'qux',
             'ARTISTS': ['q', 'u', 'x']}}
    expects = [
        ['metaflac', '--remove-all-tags', path],
        ['metaflac', '--no-utf8-convert', '--set-tag=ALBUM=foo', path],
        ['metaflac', '--no-utf8-convert', '--set-tag=ALBUMARTIST=bar', path],
        ['metaflac', '--no-utf8-convert', '--set-tag=TITLE=baz', path],
        ['metaflac', '--no-utf8-convert', '--set-tag=ARTIST=qux', path],
        ['metaflac', '--no-utf8-convert', '--set-tag=ARTISTS=q', path],
        ['metaflac', '--no-utf8-convert', '--set-tag=ARTISTS=u', path],
        ['metaflac', '--no-utf8-convert', '--set-tag=ARTISTS=x', path],
        ]

    def mock_check_call(args):
        assert args in expects
        expects.pop(expects.index(args))
        return 0

    monkeypatch.setattr(subprocess, 'check_call', mock_check_call)

    flac.write(path, tag)
