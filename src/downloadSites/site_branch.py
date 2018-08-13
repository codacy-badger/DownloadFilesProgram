# -*- coding: utf-8 -*-
from .sites import xbooks_to     # NOQA
from .sites import hentaihaven_org   # NOQA
from .sites import sugumiru18_com    # NOQA
from .sites import redtube_com   # NOQA
from .sites import moeimg_net    # NOQA
from .sites import muchaero_net  # NOQA
from .sites import nijibondo_com # NOQA
from .sites import erobooks_net  # NOQA
from .sites import pornhub_com   # NOQA
from .sites import okkisokuho_com    # NOQA
from .sites import xnxx_com  # NOQA
from .sites import xvideos_com   # NOQA
from .sites import wakusoku  # NOQA
from .sites import xhamster_com  # NOQA


class DownloadList(object):
    """docstring for DownloadList"""
    def __init__(self, url, limit=None):
        super(DownloadList, self).__init__()
        self.file_status = self.get_file_status(url, limit)

    def get_file_status(self, url, limit=None):
        url_array = self.split_url(url)
        if url_array[0] == 'xbooks.to':
            print('xbooks')
            file_status = xbooks_to.Run(url, url_array, limit).file_status
        elif url_array[0] == 'www.xvideos.com':
            print('xvideos')
            file_status = xvideos_com.Run(url, url_array).file_status
        elif url_array[0] == 'www.xnxx.com':
            print('xnxx')
            file_status = xnxx_com.Run(url, url_array).file_status
        elif url_array[0] == 'hentaihaven.org':
            print('hentaihaven')
            file_status = hentaihaven_org.Run(url, url_array).file_status
        elif url_array[0] == 'blog.livedoor.jp':
            if url_array[1] == 'wakusoku':
                print('wakusoku')
                file_status = wakusoku.Run(url, url_array, limit).file_status
        elif url_array[0] == 'xhamster.com':
            print('XHamster')
            file_status = xhamster_com.Run(url, url_array).file_status
        elif url_array[0] == 'sugumiru18.com':
            print('sugumiru18')
            file_status = sugumiru18_com.Run(url, url_array, limit).file_status
        elif url_array[0] == 'www.redtube.com':
            print('REDTUBE')
            file_status = redtube_com.Run(url, url_array).file_status
        elif url_array[0] == 'moeimg.net':
            print('moeimg')
            file_status = moeimg_net.Run(url, url_array, limit).file_status
        elif url_array[0] == 'muchaero.net':
            print('muchaero')
            file_status = muchaero_net.Run(url, url_array, limit).file_status
        elif url_array[0] == 'erobooks.net':
            print('erobooks')
            file_status = erobooks_net.Run(url, url_array, limit).file_status
        elif url_array[0] == 'nijibondo.com':
            print('nijibondo')
            file_status = nijibondo_com.Run(url, url_array, limit).file_status
        elif url_array[0] == 'okkisokuho.com':
            print('okkisokuho')
            file_status = okkisokuho_com.Run(url, url_array, limit).file_status
        elif url_array[0] == 'www.pornhub.com':
            print('pornhub')
            file_status = pornhub_com.Run(url, url_array).file_status
        return file_status

    def split_url(self, url):
        url = url.replace('https', 'http')
        url = url.replace('http://', '')
        url_array = url.split('/')
        return url_array
