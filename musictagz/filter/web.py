# encoding: utf-8
"""Tag filtering from web."""

import re
from pyquery import PyQuery as pq
from musictagz import tagtype


def touhouwiki(title, data):
    """Apply touhouwiki markup to tag."""
    d = pq(url='https://en.touhouwiki.net/'
               'index.php?title={}&action=edit'.format(title))
    markup = d('#wpTextbox1').text()
    tag = None

    def _delang(string):
        return re.sub('{{lang\|ja\|([^}]+)}}', r'\1', string)

    def _desource(string):
        if string.startswith('{{') and string.endswith('}}'):
            source = string[2:-2]
            mappings = {
                'UFO': u'東方星蓮船　～ Undefined Fantastic Object',
                'MoF': u'東方風神録　～ Mountain of Faith',
                'PoFV': u'東方花映塚　～ Phantasmagoria of Flower View',
                'DS': u'ダブルスポイラー　～ 東方文花帖',
                'PCB': u'東方妖々夢　～ Perfect Cherry Blossom',
                'EoSD': u'東方紅魔郷　～ the Embodiment of Scarlet Devil',
                'SA': u'東方地霊殿　～ Subterranean Animism',
                'IN': u'東方永夜抄　～ Imperishable Night',
                'MS': u'東方怪綺談　～ Mystic Square',
                'HRtP': u'東方靈異伝　～ Highly Responsive to Prayers',
                'HM': u'東方心綺楼　～ Hopeless Masquerade',
                'SoEW': u'東方封魔録　～ Story of Eastern Wonderland',
            }
            if source in mappings:
                return mappings[source]
        return string

    def _split_nowiki(string, splitter):
        nowiki = False
        nowiki_item = []
        for item in string.split(splitter):
            if '<nowiki>' in item:
                nowiki = True
                nowiki_item = [item.replace('<nowiki>', '')]
                continue
            if not nowiki:
                yield item
                continue
            if '</nowiki>' in item:
                nowiki_item.append(item.replace('</nowiki>', ''))
                nowiki = False
                yield splitter.join(nowiki_item)
                nowiki_item = []

            if nowiki:
                nowiki_item.append(item)

    for line in markup.splitlines():
        if '{{Track|' in line:
            tag = _find_track(data, line.split('|')[1])
            value = list(_split_nowiki(line, '|'))[2]
            tag[tagtype.PLAIN]['TITLE'] = value
        if 'website ' in line:
            value = line.split('website ', 1)[1].split('=', 1)[1]
            _apply_all(data, 'WEBSITE', value[1:-6])
        if 'catalogno ' in line:
            value = line.split('catalogno ', 1)[1].split('=', 1)[1]
            _apply_all(data, 'CATALOGNUMBER', value)
        if 'released ' in line:
            value = line.split('released ', 1)[1].split('=', 1)[1].replace('-', '.')
            _apply_all(data, 'DATE', value)
            _apply_all(data, 'ORIGINALDATE', value)
            _apply_all(data, 'ORIGINALYEAR', value.split('.')[0])
        if 'groupCat ' in line:
            value = line.split('groupCat ', 1)[1].split('=', 1)[1]
            _apply_all(data, 'ALBUMARTIST', value)
            _apply_all(data, 'LABEL', value)
        if tag and 'composition: ' in line:
            value = line.split('composition: ', 1)[1]
            tag[tagtype.PLAIN]['COMPOSER'] = _delang(value)
        if tag and 'arrangement: ' in line:
            value = line.split('arrangement: ', 1)[1]
            tag[tagtype.PLAIN]['ARRANGER'] = _delang(value)
        if tag and 'remix: ' in line:
            value = line.split('remix: ', 1)[1]
            tag[tagtype.PLAIN]['REMIXER'] = _delang(value)
        if tag and 'original title: ' in line:
            value = line.split('original title: ', 1)[1]
            tag[tagtype.PLAIN]['ORIGINALTITLE'] = _delang(value) 
        if tag and 'source: ' in line:
            value = line.split('source: ', 1)[1]
            tag[tagtype.PLAIN]['SOURCE'] = _desource(value) 
        if tag and 'lyrics: ' in line:
            value = line.split('lyrics: ', 1)[1]
            tag[tagtype.PLAIN]['LYRICIST'] = _delang(value) 
        if tag and 'vocals: ' in line:
            value = line.split('vocals: ', 1)[1]
            if 'PERFORMER' in tag[tagtype.PLAIN]:
                if isinstance(tag[tagtype.PLAIN]['PERFORMER'], str):
                    tag[tagtype.PLAIN]['PERFORMER'] = list(
                        tag[tagtype.PLAIN]['PERFORMER'])
            else:
                tag[tagtype.PLAIN]['PERFORMER'] = []
            value = _delang(value) + ' (vocals)'
            if value not in tag[tagtype.PLAIN]['PERFORMER']:
                tag[tagtype.PLAIN]['PERFORMER'].append(value)
        if tag and 'guiter: ' in line:
            value = line.split('guiter: ', 1)[1]
            if 'PERFORMER' in tag[tagtype.PLAIN]:
                if isinstance(tag[tagtype.PLAIN]['PERFORMER'], str):
                    tag[tagtype.PLAIN]['PERFORMER'] = list(
                        tag[tagtype.PLAIN]['PERFORMER'])
            else:
                tag[tagtype.PLAIN]['PERFORMER'] = []
            value = _delang(value) + ' (guiter)'
            if value not in tag[tagtype.PLAIN]['PERFORMER']:
                tag[tagtype.PLAIN]['PERFORMER'].append(value)
    return data

def _find_track(data, track):
    for filename, tag in data.iteritems():
        if int(tag[tagtype.PLAIN]['TRACKNUMBER']) == int(track):
            return tag

def _apply_all(data, key, value):
    for filename, tag in data.iteritems():
        tag[tagtype.PLAIN][key] = value
