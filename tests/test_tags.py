import glob
from musictagz import tags
from musictagz.codecs import auto


def test_flatten(monkeypatch):
    data = {
        '*.flac':
            {'plain':
                {'ALBUM': 'foo',
                 'ALBUMARTIST': 'bar'}},
        './01*.flac':
            {'plain':
                {'TITLE': 'baz',
                 'ARTIST': 'qux',
                 'ARTISTS': ['q', 'u', 'x']}},
        './02*.flac':
            {'plain':
                {'TITLE': 'foobar',
                 'ARTIST': 'quux',
                 'ARTISTS': ['q', 'uu', 'x']}},
    }

    def mock_glob_glob(pattern):
        ans = {'*.flac': ['01 baz.flac', '02 foobar.flac'],
               './01*.flac': ['./01 baz.flac'],
               './02*.flac': ['./02 foobar.flac']}
        assert pattern in ans
        return ans[pattern]

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


def test_deflatten():
    flatten_data = {
        '01 baz.flac':
            {'plain':
                {'TITLE': 'baz',
                 'ALBUM': 'foo'}},
        '02 foobar.flac':
            {'plain':
                {'TITLE': 'foobar',
                 'ALBUM': 'foo'}}
    }
    expect = {
        '*.flac':
            {'plain': {'ALBUM': 'foo'}},
        '01 baz.flac':
            {'plain':
                {'TITLE': 'baz'}},
        '02 foobar.flac':
            {'plain':
                {'TITLE': 'foobar'}}
    }
    assert expect == tags.deflatten(flatten_data)


def test_search_same_key_value():
    flatten_data = {
        '01 baz.flac':
            {'plain':
                {'TITLE': 'baz',
                 'ALBUM': 'foo'}},
        '02 foobar.flac':
            {'plain':
                {'TITLE': 'foobar',
                 'ALBUM': 'foo'}}
    }
    assert {'plain':
            {'ALBUM': 'foo'}} == tags.search_same_key_value(flatten_data)


def test_globbing_path():
    flatten_data = {
        '01 baz.flac':
            {'plain':
                {'TITLE': 'baz'}},
        '02 foobar.flac':
            {'plain':
                {'TITLE': 'foobar'}}
    }
    assert '*.flac' == tags.globbing_path(flatten_data)

    flatten_data = {
        'disc01-01 baz.flac':
            {'plain':
                {'TITLE': 'baz'}},
        'disc01-02 foobar.flac':
            {'plain':
                {'TITLE': 'foobar'}}
    }
    assert 'disc01-0*.flac' == tags.globbing_path(flatten_data)

    flatten_data = {
        'disc01-01 foo-baz.flac':
            {'plain':
                {'TITLE': 'baz'}},
        'disc01-02 foo-foobar.flac':
            {'plain':
                {'TITLE': 'foobar'}}
    }
    assert 'disc01-0*foo*.flac' == tags.globbing_path(flatten_data)
