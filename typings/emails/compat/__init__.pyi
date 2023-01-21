"""
This type stub file was generated by pyright.
"""

import sys
import urlparse
import urllib.parse as urlparse
from __future__ import unicode_literals
from .orderedset import OrderedSet
from .ordereddict import OrderedDict
from StringIO import StringIO
from cStringIO import StringIO as BytesIO
from email.utils import escapesre, formataddr, specialsre
from collections import OrderedDict
from io import BytesIO, StringIO

_ver = ...
is_py2 = ...
is_py3 = ...
is_py30 = ...
is_py31 = ...
is_py32 = ...
is_py33 = ...
is_py34 = ...
is_py34_plus = ...
is_py27 = ...
is_py26 = ...
is_py25 = ...
is_py24 = ...
_ver = ...
is_pypy = ...
is_jython = ...
is_ironpython = ...
is_cpython = ...
is_windows = ...
is_linux = ...
is_osx = ...
is_hpux = ...
is_solaris = ...
if is_py2:
    unichr = ...
    text_type = ...
    string_types = ...
    integer_types = ...
    int_to_byte = ...
    NativeStringIO = ...
    def to_native(x, charset=..., errors=...): # -> str:
        ...

    def is_callable(x): # -> bool:
        ...

    def to_bytes(x, charset=..., errors=...): # -> bytes | None:
        ...

else:
    NativeStringIO = ...
    unichr = ...
    text_type = ...
    string_types = ...
    integer_types = ...
    def to_native(x, charset=..., errors=...): # -> str:
        ...

    def is_callable(x): # -> bool:
        ...

    def to_bytes(x, charset=..., errors=...): # -> bytes | None:
        ...

    def formataddr(pair): # -> LiteralString:
        """
        This code is copy of python2 email.utils.formataddr.
        Takes a 2-tuple of the form (realname, email_address) and returns RFC2822-like string.
        Does not encode non-ascii realname.

        Python3 email.utils.formataddr do encode realname.
        """
        ...

def to_unicode(x, charset=..., errors=..., allow_none_charset=...): # -> str | bytes | None:
    ...