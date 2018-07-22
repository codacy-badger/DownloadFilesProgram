#!/usr/bin/python
# -*- coding: utf-8 -*-


class Codec(object):
    """docstring for Codec"""
    def __init__(self):
        super(Codec, self).__init__()

    # code -> utf-8
    def to_utf8(self, chars):
        chars_type = str(type(chars))
        chars_type = chars_type.split("'")[1]
        if chars_type == 'str':
            return chars
        elif chars_type == 'unicode':
            return chars.encode('utf-8')
        elif chars_type == 'euc-jp':
            chars = chars.decode('euc-jp')
            return chars.encode('utf-8')
        else:
            print "encode error: " + chars_type
            return str(chars)

    # code -> unicode
    def to_unicode(self, chars):
        chars_type = str(type(chars))
        chars_type = chars_type.split("'")[1].strip()
        if chars_type == 'str':
            return chars.decode('utf-8')
        elif chars_type == 'unicode':
            return chars
        elif chars_type == 'euc-jp':
            return chars.decode('euc-jp')
        else:
            print "decode error: " + chars_type
            return chars
