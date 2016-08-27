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
COMMENT=\xe3\x81\xbb\xe3\x81\x92
LINEFEEDTEST=abc
def
LINEFEEDTEST=ghi
jkl
'''
    monkeypatch.setattr(subprocess, 'check_output', mock_check_output)
    expect = {
        tagtype.PLAIN:
            {u'ALBUM': u'foo',
             u'ALBUMARTIST': u'bar',
             u'TITLE': u'baz',
             u'ARTIST': u'qux',
             u'ARTISTS': [u'q', u'u', u'x'],
             u'COMMENT': '\xe3\x81\xbb\xe3\x81\x92'.decode('utf-8'),
             u'LINEFEEDTEST': [u'abc\ndef', u'ghi\njkl']
             }
    }
    assert expect == flac.read('01.flac')


def test_write(monkeypatch):
    path = '01.flac'
    tag = {
        tagtype.PLAIN:
            {u'ALBUM': u'foo',
             u'ALBUMARTIST': u'bar',
             u'TITLE': u'baz',
             u'ARTIST': u'qux',
             u'ARTISTS': [u'q', u'u', u'x'],
             u'COMMENT': '\xe3\x81\xbb\n\xe3\x81\x92'.decode('utf-8')}}
    expects = [
        ['metaflac', '--remove-all-tags', path],
        ['metaflac', '--no-utf8-convert',
         '--set-tag=COMMENT=\xe3\x81\xbb\n\xe3\x81\x92', path],
        ]

    def mock_check_call(args):
        assert args in expects
        expects.pop(expects.index(args))
        return 0

    class MockPopen(object):
        def __init__(self, cmd, stdin=None):
            assert cmd == ['metaflac', '--no-utf8-convert',
                           '--import-tags-from=-', '01.flac']
            assert stdin == subprocess.PIPE

        def communicate(self, input=None):
            expects = ['ALBUM=foo',
                       'ALBUMARTIST=bar',
                       'TITLE=baz',
                       'ARTIST=qux',
                       'ARTISTS=q',
                       'ARTISTS=u',
                       'ARTISTS=x']
            assert len(expects) == len(input.splitlines())
            assert input.endswith('\n')
            for expect in expects:
                assert expect in input

        def wait(self):
            pass

    monkeypatch.setattr(subprocess, 'check_call', mock_check_call)
    monkeypatch.setattr(subprocess, 'Popen', MockPopen)

    flac.write(path, tag)
