from musictagz.codecs import auto, flac, error
import pytest


def test_detect_codec_flac(monkeypatch):
    def mock_flac_checktype(path):
        assert path == '01.flac'
        return True

    monkeypatch.setattr(flac, 'checktype', mock_flac_checktype)
    assert flac == auto.detect('01.flac')


def test_detect_codec_error(monkeypatch):
    def mock_flac_checktype(path):
        return False

    monkeypatch.setattr(flac, 'checktype', mock_flac_checktype)
    with pytest.raises(error.UnsupportedCodecError):
        auto.detect('01.ogg')


def test_read(monkeypatch):
    def mock_detect(path):
        assert '01.flac' == path

        class MockCodec(object):
            def read(self, path):
                assert '01.flac' == path
                return {'TRACKNUMBER': '1'}

        return MockCodec()

    monkeypatch.setattr(auto, 'detect', mock_detect)
    assert {'TRACKNUMBER': '1'} == auto.read('01.flac')


def test_write(monkeypatch):
    def mock_detect(path):
        assert '01.flac' == path

        class MockCodec(object):
            def write(self, path, tag):
                assert '01.flac' == path
                assert {'TRACKNUMBER': '1'} == tag

        return MockCodec()

    monkeypatch.setattr(auto, 'detect', mock_detect)
    auto.write('01.flac', {'TRACKNUMBER': '1'})
