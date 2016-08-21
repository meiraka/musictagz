import glob
from musictagz import tags
from musictagz.codecs import auto


def test_flatten(monkeypatch):
    data = {
        '*.flac':
            {'plain':
                {'ALBUM': 'foo',
                 'ALBUMARTIST': 'bar'}},
        '01*.flac':
            {'plain':
                {'TITLE': 'baz',
                 'ARTIST': 'qux',
                 'ARTISTS': ['q', 'u', 'x']}},
        '02*.flac':
            {'plain':
                {'TITLE': 'foobar',
                 'ARTIST': 'quux',
                 'ARTISTS': ['q', 'uu', 'x']}},
    }

    def mock_glob_glob(pattern):
        if pattern == '*.flac':
            return ['01 baz.flac', '02 foobar.flac']
        elif pattern == '01*.flac':
            return ['01 baz.flac']
        else:
            return ['02 foobar.flac']

    expect = {
        '01 baz.flac':
            {'plain':
                {'ALBUM': 'foo',
                 'ALBUMARTIST': 'bar',
                 'TITLE': 'baz',
                 'ARTIST': 'qux',
                 'ARTISTS': ['q', 'u', 'x']}},
        '02 foobar.flac':
            {'plain':
                {'ALBUM': 'foo',
                 'ALBUMARTIST': 'bar',
                 'TITLE': 'foobar',
                 'ARTIST': 'quux',
                 'ARTISTS': ['q', 'uu', 'x']}}
    }

    monkeypatch.setattr(glob, 'glob', mock_glob_glob)
    assert expect == tags.flatten(data)


def test_write(monkeypatch):
    flatten_data = {
        '01 baz.flac':
            {'plain':
                {'TITLE': 'baz'}},
        '02 foobar.flac':
            {'plain':
                {'TITLE': 'foobar'}}
    }

    expects = [
        ('01 baz.flac', {'plain': {'TITLE': 'baz'}}),
        ('02 foobar.flac', {'plain': {'TITLE': 'foobar'}})
    ]

    def mock_auto_write(path, tag):
        assert (path, tag) in expects
        expects.pop(expects.index((path, tag)))

    monkeypatch.setattr(auto, 'write', mock_auto_write)

    tags.write(flatten_data)
