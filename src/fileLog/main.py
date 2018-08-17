# -*- coding: utf-8 -*-
import os

from .codec import Codec


class URLlog(object):
    """docstring for URLlog"""
    def __init__(self, logdir, url):
        super(URLlog, self).__init__()
        self.parentdir = logdir
        self.url = url

    def check_log(self, add_url=False):
        logpath = self._get_log_path(self.parentdir)
        if self._exist_url(logpath, self.url):
            return True
        else:
            if add_url:
                self._add_url(logpath, self.url)
            return False

    def _get_log_path(self, parentdir):
        dl_log = os.path.join(parentdir, '__DLlog__.txt')
        return dl_log

    def _exist_url(self, fpath, url):
        urls = ''
        try:
            with open(fpath, mode='r') as f:
                urls = f.read()
        except:
            with open(fpath, mode='w') as f:
                pass
        urls = Codec().to_utf8(urls)
        return True if url in urls else False

    def _add_url(self, fpath, url):
        with open(fpath, mode='a') as f:
            f.write(url + '\n')
