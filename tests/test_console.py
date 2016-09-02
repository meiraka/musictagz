import sys

from musictagz import console
from musictagz import tags


def test_main_dump(monkeypatch):
    def mock_dump_yaml(glob_path):
        assert './*' == glob_path

    monkeypatch.setattr(console, 'dump_yaml', mock_dump_yaml)

    assert 0 == console.main(['--dump'])
    assert 0 == console.main(['-d'])


def test_main_load(monkeypatch):
    def mock_load_yaml():
        pass

    monkeypatch.setattr(console, 'load_yaml', mock_load_yaml)

    assert 0 == console.main(['--load'])
    assert 0 == console.main(['-l'])
    assert 0 == console.main([])


def test_main_rewrite(monkeypatch):
    def mock_rewrite():
        pass

    monkeypatch.setattr(console, 'rewrite', mock_rewrite)

    assert 0 == console.main(['--rewrite'])
    assert 0 == console.main(['-r'])


def test_dump_yaml(monkeypatch):
    def mock_tags_read(glob_path):
        assert './*' == glob_path
        return {'01.flac': {'plain': {'TEST': 'TEST'}}}

    def mock_tags_deflatten(flatten_data):
        assert {'01.flac': {'plain': {'TEST': 'TEST'}}} == flatten_data
        return {'*.flac': {'plain': {'TEST': 'TEST'}}}

    class MockStdout(object):
        def __init__(self):
            pass

        def write(self, data):
            assert ''''*.flac':
  plain:
    TEST: TEST
''' == data

    monkeypatch.setattr(tags, 'read', mock_tags_read)
    monkeypatch.setattr(tags, 'deflatten', mock_tags_deflatten)
    monkeypatch.setattr(sys, 'stdout', MockStdout())
    assert 0 == console.dump_yaml('./*')


def test_load_yaml(monkeypatch):
    def mock_tags_flatten(data):
        assert {'*.flac': {'plain': {'TEST': 'TEST'}}} == data
        return {'01.flac': {'plain': {'TEST': 'TEST'}}}

    def mock_tags_write(flatten_data):
        assert {'01.flac': {'plain': {'TEST': 'TEST'}}} == flatten_data

    class MockStdin(object):
        def __init__(self):
            pass

        def read(self):
            return ''''*.flac':
  plain:
    TEST: TEST
'''

    monkeypatch.setattr(tags, 'write', mock_tags_write)
    monkeypatch.setattr(tags, 'flatten', mock_tags_flatten)
    monkeypatch.setattr(sys, 'stdin', MockStdin())
    assert 0 == console.load_yaml()
