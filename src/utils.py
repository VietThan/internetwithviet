from collections import abc
BASIC_TYPES = (int, float, complex, bool, str, bytes)

# modified off https://stackoverflow.com/a/15836901
def dict_merge(a, b):
    """
    merges b into a and return merged result

    NOTE: tuples and arbitrary objects are not handled as it is totally ambiguous what should happen
    """
    key = None
    try:
        if a is None or isinstance(a, BASIC_TYPES):
            # border case for first run or if a is a primitive
            a = b
        elif isinstance(a, list):
            # lists can be only appended
            if isinstance(b, abc.Sequence):
                # merge lists
                a.extend(b)
            else:
                # append to list
                a.append(b)
        elif isinstance(a, abc.MutableMapping):
            # dicts must be merged
            if isinstance(b, abc.Mapping):
                for key in b:
                    if key in a:
                        a[key] = dict_merge(a[key], b[key])
                    else:
                        a[key] = b[key]
            else:
                raise AssertionError(f'Cannot merge non-dict "{b}" into dict "{a}"')
        else:
            raise AssertionError(f'NOT IMPLEMENTED "{b}" into "{a}"')
    except TypeError as e:
        raise AssertionError(f'TypeError "{e}" in key "{key}" when merging "{b}" into "{a}"')
    return a