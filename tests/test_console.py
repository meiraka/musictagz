import sys

from musictagz import console
from musictagz import tags


def test_main_dump(monkeypatch):
    def mock_read_from_music_file(glob_path):
        assert './*' == glob_path
        return {'01.flac': {'plain': {'TEST': 'TEST'}}}

    def mock_write_to_yaml_file(f, flatten_data):
        assert sys.stdout == f
        assert {'01.flac': {'plain': {'TEST': 'TEST'}}} == flatten_data
        return 0

    monkeypatch.setattr(console, 'read_from_music_file',
                        mock_read_from_music_file)
    monkeypatch.setattr(console, 'write_to_yaml_file',
                        mock_write_to_yaml_file)

    assert 0 == console.main(['--dump'])
    assert 0 == console.main(['-d'])


def test_main_load(monkeypatch):
    def mock_read_from_yaml_file(f):
        assert sys.stdin == f
        return {'01.flac': {'plain': {'TEST': 'TEST'}}}

    def mock_write_to_music_file(flatten_data):
        assert {'01.flac': {'plain': {'TEST': 'TEST'}}} == flatten_data
        return 0

    monkeypatch.setattr(console, 'read_from_yaml_file',
                        mock_read_from_yaml_file)
    monkeypatch.setattr(console, 'write_to_music_file',
                        mock_write_to_music_file)

    assert 0 == console.main(['--load'])
    assert 0 == console.main(['-l'])
    assert 0 == console.main([])


def test_main_rewrite(monkeypatch):
    def mock_read_from_yaml_file(f):
        assert sys.stdin == f
        return {'01.flac': {'plain': {'TEST': 'TEST'}}}

    def mock_write_to_yaml_file(f, flatten_data):
        assert sys.stdout == f
        assert {'01.flac': {'plain': {'TEST': 'TEST'}}} == flatten_data
        return 0

    monkeypatch.setattr(console, 'read_from_yaml_file',
                        mock_read_from_yaml_file)
    monkeypatch.setattr(console, 'write_to_yaml_file',
                        mock_write_to_yaml_file)

    assert 0 == console.main(['--rewrite'])
    assert 0 == console.main(['-r'])
    assert 0 == console.main(['--dryrun'])
    assert 0 == console.main(['-n'])
    assert 0 == console.main(['--filter'])


def test_read_from_yaml_file():
    request = ''''*.flac':
  plain:
    TEST: TEST
'''
    expect = {'*.flac': {'plain': {'TEST': 'TEST'}}}

    class MockStdin(object):
        def __init__(self):
            pass

        def read(self):
            return request

    assert expect == console.read_from_yaml_file(MockStdin())


def test_read_from_music_file(monkeypatch):
    request = './*'
    expect = {'*.flac': {'plain': {'TEST': 'TEST'}}}

    def mock_tags_read(glob_path):
        assert request == glob_path
        return {'01.flac': {'plain': {'TEST': 'TEST'}}}

    def mock_tags_deflatten(flatten_data):
        assert {'01.flac': {'plain': {'TEST': 'TEST'}}} == flatten_data
        return expect

    monkeypatch.setattr(tags, 'read', mock_tags_read)
    monkeypatch.setattr(tags, 'deflatten', mock_tags_deflatten)
    assert expect == console.read_from_music_file(request)


def test_write_to_yaml_file():
    request = {'*.flac': {'plain': {'TEST': 'TEST'}}}

    class MockStdout(object):
        def __init__(self):
            pass

        def write(self, data):
            assert ''''*.flac':
  plain:
    TEST: TEST
''' == data

    assert 0 == console.write_to_yaml_file(MockStdout(), request)


def test_write_to_music_file(monkeypatch):
    request = {'*.flac': {'plain': {'TEST': 'TEST'}}}

    def mock_tags_flatten(data):
        assert request == data
        return {'01.flac': {'plain': {'TEST': 'TEST'}}}

    def mock_tags_write(flatten_data):
        assert {'01.flac': {'plain': {'TEST': 'TEST'}}} == flatten_data

    monkeypatch.setattr(tags, 'write', mock_tags_write)
    monkeypatch.setattr(tags, 'flatten', mock_tags_flatten)
    assert 0 == console.write_to_music_file(request)
