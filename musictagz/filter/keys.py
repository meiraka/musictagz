import copy

from musictagz import tagtype


def _exec_filter(data, filter_func, mode='move', overwrite=True):
    new_data = copy.deepcopy(data)
    for path, ttkv in data.iteritems():
        for tt, kv in ttkv.iteritems():
            if tt != tagtype.PLAIN:
                continue
            for key, value in kv.iteritems():
                new_key = filter_func(key)
                if new_key == key:
                    continue
                if overwrite or new_key not in new_data[path][tt]:
                    new_data[path][tt][new_key] = value
                if mode == 'move':
                    del new_data[path][tt][key]
    return new_data


def upper(data, overwrite=True):
    """Return a copy of the data that given keys are upper cased.

    if overwrite, exists uppercase key is overwritten by new value.
    >>> data = {'01.flac': {'plain': {'albumartist': 'Hoge',
    ...                               'ALBUMARTIST': 'hoge'}}}
    >>> upper(data, overwrite=True)
    {'01.flac': {'plain': {'ALBUMARTIST': 'Hoge'}}}

    if not overwrite and exists uppercase key, remove lowercase value.
    >>> upper(data, overwrite=False)
    {'01.flac': {'plain': {'ALBUMARTIST': 'hoge'}}}
    """
    def _upper(string):
        return string.upper()
    return _exec_filter(data, _upper, 'move', overwrite)


def lower(data, overwrite=True):
    """Return a copy of the data that given keys are lower cased.

    if overwrite, exists lowercase key is overwritten by new value.
    >>> data = {'01.flac': {'plain': {'albumartist': 'Hoge',
    ...                               'ALBUMARTIST': 'hoge'}}}
    >>> lower(data, overwrite=True)
    {'01.flac': {'plain': {'albumartist': 'hoge'}}}

    if not overwrite and exists lowercase key, remove lowercase value.
    >>> lower(data, overwrite=False)
    {'01.flac': {'plain': {'albumartist': 'Hoge'}}}
    """
    def _lower(string):
        return string.lower()
    return _exec_filter(data, _lower, 'move', overwrite)
