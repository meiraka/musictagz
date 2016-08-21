from musictagz import console


def test_main_dump(monkeypatch):
    def mock_dump_yaml(glob_path, yaml_path):
        assert './*' == glob_path
        assert './tracks.yml' == yaml_path

    monkeypatch.setattr(console, 'dump_yaml', mock_dump_yaml)

    assert 0 == console.main(['--dump'])
    assert 0 == console.main(['-d'])


def test_main_load(monkeypatch):
    def mock_load_yaml(yaml_path):
        assert './tracks.yml' == yaml_path

    monkeypatch.setattr(console, 'load_yaml', mock_load_yaml)

    assert 0 == console.main(['--load'])
    assert 0 == console.main(['-l'])
    assert 0 == console.main([])
