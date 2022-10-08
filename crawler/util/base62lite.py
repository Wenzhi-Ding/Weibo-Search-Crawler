# -*- coding: utf-8 -*-
"""
base62
~~~~~~

Originated from http://blog.suminb.com/archives/558
"""

__title__ = "base62"
__author__ = "Sumin Byeon"
__email__ = "suminb@gmail.com"
__version__ = "0.5.0"

BASE = 62
CHARSET_DEFAULT = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
CHARSET_INVERTED = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

string_types = (str,)
bytes_types = (bytes,)

def encode(n, minlen=1, charset=CHARSET_DEFAULT):
    """Encodes a given integer ``n``."""

    chs = []
    while n > 0:
        r = n % BASE
        n //= BASE

        chs.append(charset[r])

    if len(chs) > 0:
        chs.reverse()
    else:
        chs.append("0")

    s = "".join(chs)
    s = charset[0] * max(minlen - len(s), 0) + s
    return s


def decode(encoded, charset=CHARSET_DEFAULT):
    """Decodes a base62 encoded value ``encoded``.

    :type encoded: str
    :rtype: int
    """
    _check_type(encoded, string_types)

    if encoded.startswith("0z"):
        encoded = encoded[2:]

    l, i, v = len(encoded), 0, 0
    for x in encoded:
        v += _value(x, charset=charset) * (BASE ** (l - (i + 1)))
        i += 1

    return v


def _value(ch, charset):
    """Decodes an individual digit of a base62 encoded string."""

    try:
        return charset.index(ch)
    except ValueError:
        raise ValueError("base62: Invalid character (%s)" % ch)


def _check_type(value, expected_type):
    """Checks if the input is in an appropriate type."""

    if not isinstance(value, expected_type):
        msg = "Expected {} object, not {}".format(
            expected_type, value.__class__.__name__
        )
        raise TypeError(msg)
