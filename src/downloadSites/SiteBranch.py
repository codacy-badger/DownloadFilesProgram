# -*- coding: utf-8 -*-

from . import dropBOOKS_tv
from . import Xvideos_com
from . import xnxx_com
from . import AnimeHaven_org
from . import wakusoku
from . import Xhamster_com
from . import lolig_blog
from . import sugumiru18_com
from . import HentaiHaven_org
from . import REDTUBE_com
from . import moeimg_net
from . import muchaero_net
from . import nijibondo_com
from . import nizigazo_net
from . import okkisokuho_com
from . import Pornhub_com


class DownloadList(object):
    """docstring for DownloadList"""
    def __init__(self, url, limit=None):
        super(DownloadList, self).__init__()
        self.fileStatus = self.getFileStatus(url, limit)

    def getFileStatus(self, url, limit=None):
        urlArray = self.splitURL(url)
        if urlArray[0] == 'dlbooks.to':
            print('dropbooks')
            fileStatus = dropBOOKS_tv.run(url, urlArray, limit).filestatus
        elif urlArray[0] == 'www.xvideos.com':
            print('xvideos')
            fileStatus = Xvideos_com.run(url, urlArray).filestatus
        elif urlArray[0] == 'www.xnxx.com':
            print('xnxx')
            fileStatus = xnxx_com.run(url, urlArray).filestatus
        elif urlArray[0] == 'animehaven.org' or urlArray[0] == 'animehaven.to':
            print('animehaven')
            fileStatus = AnimeHaven_org.run(url, urlArray).filestatus
        elif urlArray[0] == 'hentaihaven.org':
            print('hentaihaven')
            fileStatus = HentaiHaven_org.run(url, urlArray).filestatus
        elif urlArray[0] == 'blog.livedoor.jp':
            if urlArray[1] == 'wakusoku':
                print('wakusoku')
                fileStatus = wakusoku.run(url, urlArray, limit).filestatus
        elif urlArray[0] == 'xhamster.com':
            print('XHamster')
            fileStatus = Xhamster_com.run(url, urlArray).filestatus
        elif urlArray[0] == 'lolig.blog.jp':
            print('lolig')
            fileStatus = lolig_blog.run(url, urlArray, limit).filestatus
        elif urlArray[0] == 'sugumiru18.com':
            print('sugumiru18')
            fileStatus = sugumiru18_com.run(url, urlArray, limit).filestatus
        elif urlArray[0] == 'www.redtube.com':
            print('REDTUBE')
            fileStatus = REDTUBE_com.run(url, urlArray).filestatus
        elif urlArray[0] == 'moeimg.net':
            print('moeimg')
            fileStatus = moeimg_net.run(url, urlArray, limit).filestatus
        elif urlArray[0] == 'muchaero.net':
            print('muchaero')
            fileStatus = muchaero_net.run(url, urlArray, limit).filestatus
        elif urlArray[0] == 'nizigazo.net':
            print('nizigazo')
            fileStatus = nizigazo_net.run(url, urlArray, limit).filestatus
        elif urlArray[0] == 'nijibondo.com':
            print('nijibondo')
            fileStatus = nijibondo_com.run(url, urlArray, limit).filestatus
        elif urlArray[0] == 'okkisokuho.com':
            print('okkisokuho')
            fileStatus = okkisokuho_com.run(url, urlArray, limit).filestatus
        elif urlArray[0] == 'www.pornhub.com' or urlArray[0] == 'jp.pornhub.com':
            print('pornhub')
            fileStatus = Pornhub_com.run(url, urlArray).filestatus
        return fileStatus

    def splitURL(self, url):
        url = url.replace('https', 'http')
        url = url.replace('http://', '')
        urlArray = url.split('/')
        return urlArray
