"""Add template key/value."""

from musictagz import tagtype


def musicbrainz(data):
    """Add muscic brainz tag template.

    https://picard.musicbrainz.org/docs/mappings/
    """
    for filename, tag in data.iteritems():
        _copy_if(tag, 'ORIGINALDATE', 'DATE')
        _write_if(tag, 'ORIGINALDATE')
        _copy_if(tag, 'ORIGINALYEAR', 'DATE')
        _write_if(tag, 'ORIGINALYEAR')
        _write_if(tag, 'CATALOGNUMBER')
        _write_if(tag, 'DISCNUMBER', '1')
        _copy_if(tag, 'DISCTOTAL', 'TOTALDISCS')
        _copy_if(tag, 'TOTALDISCS', 'DISCTOTAL')
        _write_if(tag, 'DISCTOTAL', '1')
        _write_if(tag, 'TOTALDISCS', '1')
        _write_if(tag, 'GENRE', 'unknown')
        _write_if(tag, 'LABEL')
        _write_if(tag, 'LANGUAGE', 'JP')
        _write_if(tag, 'MEDIA', 'CD')
        _write_if(tag, 'RELEASECOUNTRY', 'JP')
        _write_if(tag, 'RELEASESTATUS', 'official')
        _write_if(tag, 'RELEASETYPE', 'album / single / compilation')
        _copy_if(tag, 'TITLESORT', 'TITLE')
        _write_if(tag, 'TRACKNUMBER', '1')
        _copy_if(tag, 'TRACKTOTAL', 'TOTALTRACKS')
        _copy_if(tag, 'TOTALTRACKS', 'TRACKTOTAL')
        if 'ARTIST' not in tag[tagtype.PLAIN]:
            if 'PERFORMER' in tag[tagtype.PLAIN]:
                artist = None
                if isinstance(tag[tagtype.PLAIN]['PERFORMER'], str):
                    artist = tag[tagtype.PLAIN]['PERFORMER']
                else:
                    for line in tag[tagtype.PLAIN]['PERFORMER']:
                        if ' (vocals)' in line:
                            artist = line
                if artist and ' (vocals)' in artist:
                    tag[tagtype.PLAIN]['ARTIST'] = artist.replace(
                        ' (vocals)', '')
        _copy_if(tag, 'ARRANGER', 'ARTIST')
        _copy_if(tag, 'COMPOSER', 'ARTIST')

        _write_if(tag, 'WEBSITE')
    return data


def _copy_if(tag, src, dst):
    if src in tag[tagtype.PLAIN] and dst not in tag[tagtype.PLAIN]:
        tag[tagtype.PLAIN][dst] = tag[tagtype.PLAIN][src]


def _write_if(tag, dst, value='boilerplate'):
    if dst not in tag[tagtype.PLAIN]:
        tag[tagtype.PLAIN][dst] = '# ' + value


