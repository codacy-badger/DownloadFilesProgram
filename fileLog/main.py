#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from codec import Codec


class URLlog(object):
    """docstring for URLlog"""
    def __init__(self, logdir, url):
        super(URLlog, self).__init__()
        self.parentdir = logdir
        self.url = url

    def checkLog(self, addURL=False):
        logpath = self._getLogPath(self.parentdir)
        if self._existURL(logpath, self.url):
            return True
        else:
            if addURL:
                self._addURL(logpath, self.url)
            return False

    def _getLogPath(self, parentdir):
        dl_log = os.path.join(parentdir, '__DLlog__.txt')
        return dl_log

    def _existURL(self, fpath, url):
        urls = ''
        try:
            with open(fpath, mode='r') as f:
                urls = f.read()
        except:
            with open(fpath, mode='w') as f:
                pass
        urls = Codec().to_utf8(urls)
        return True if url in urls else False

    def _addURL(self, fpath, url):
        with open(fpath, mode='a') as f:
            f.write(url + '\n')
