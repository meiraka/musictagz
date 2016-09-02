=========
MusicTagz
=========

Yaml based audio tag editor for Flac.

Usage
=====

1. Make yaml file from audio file.

.. code:: bash

  > musictagz --dump > tracks.yaml

2. Edit yaml file.

3. Write yaml file to audio file.

.. code:: bash

  > cat tracks.yaml | musictagz


Format
======

.. code:: yaml

  '*.flac':  # filepath
    plain:  # plain text field
      ALBUM: Foo  # tag key: value
      ALBUMARTIST: Bar
  ./01 Qux.flac:
    plain:
      ARTIST: Bar and Buz
      ARTISTS:
      - Bar
      - Buz
      TITLE: Qux
      TRACKNUMBER: '1'
  ./02 Foo.flac:
    plain:
      ARTIST: Bar
      TITLE: Foo
      TRACKNUMBER: '2'
