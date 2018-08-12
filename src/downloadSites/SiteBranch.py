# -*- coding: utf-8 -*-
from . import AnimeHaven_org    # NOQA
from . import xbooks_to     # NOQA
from . import HentaiHaven_org   # NOQA
from . import lolig_blog    # NOQA
from . import sugumiru18_com    # NOQA
from . import REDTUBE_com   # NOQA
from . import moeimg_net    # NOQA
from . import muchaero_net  # NOQA
from . import nijibondo_com # NOQA
from . import nizigazo_net  # NOQA
from . import Pornhub_com   # NOQA
from . import okkisokuho_com    # NOQA
from . import xnxx_com  # NOQA
from . import Xvideos_com   # NOQA
from . import wakusoku  # NOQA
from . import Xhamster_com  # NOQA


class DownloadList(object):
    """docstring for DownloadList"""
    def __init__(self, url, limit=None):
        super(DownloadList, self).__init__()
        self.file_status = self.get_file_status(url, limit)

    def get_file_status(self, url, limit=None):
        url_array = self.split_url(url)
        if url_array[0] == 'dlbooks.to':
            print('dropbooks')
            file_status = xbooks_to.Run(url, url_array, limit).file_status
        elif url_array[0] == 'www.xvideos.com':
            print('xvideos')
            file_status = Xvideos_com.Run(url, url_array).file_status
        elif url_array[0] == 'www.xnxx.com':
            print('xnxx')
            file_status = xnxx_com.Run(url, url_array).file_status
        elif url_array[0] == 'animehaven.to':
            print('animehaven')
            file_status = AnimeHaven_org.Run(url, url_array).file_status
        elif url_array[0] == 'hentaihaven.org':
            print('hentaihaven')
            file_status = HentaiHaven_org.Run(url, url_array).file_status
        elif url_array[0] == 'blog.livedoor.jp':
            if url_array[1] == 'wakusoku':
                print('wakusoku')
                file_status = wakusoku.Run(url, url_array, limit).file_status
        elif url_array[0] == 'xhamster.com':
            print('XHamster')
            file_status = Xhamster_com.Run(url, url_array).file_status
        elif url_array[0] == 'lolig.blog.jp':
            print('lolig')
            file_status = lolig_blog.Run(url, url_array, limit).file_status
        elif url_array[0] == 'sugumiru18.com':
            print('sugumiru18')
            file_status = sugumiru18_com.Run(url, url_array, limit).file_status
        elif url_array[0] == 'www.redtube.com':
            print('REDTUBE')
            file_status = REDTUBE_com.Run(url, url_array).file_status
        elif url_array[0] == 'moeimg.net':
            print('moeimg')
            file_status = moeimg_net.Run(url, url_array, limit).file_status
        elif url_array[0] == 'muchaero.net':
            print('muchaero')
            file_status = muchaero_net.Run(url, url_array, limit).file_status
        elif url_array[0] == 'nizigazo.net':
            print('nizigazo')
            file_status = nizigazo_net.Run(url, url_array, limit).file_status
        elif url_array[0] == 'nijibondo.com':
            print('nijibondo')
            file_status = nijibondo_com.Run(url, url_array, limit).file_status
        elif url_array[0] == 'okkisokuho.com':
            print('okkisokuho')
            file_status = okkisokuho_com.Run(url, url_array, limit).file_status
        elif url_array[0] == 'www.pornhub.com':
            print('pornhub')
            file_status = Pornhub_com.Run(url, url_array).file_status
        return file_status

    def split_url(self, url):
        url = url.replace('https', 'http')
        url = url.replace('http://', '')
        url_array = url.split('/')
        return url_array
