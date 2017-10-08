#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- coding: cp932 -*-


import dropBOOKS_tv
import Xvideos_com
import AnimeHaven_org
import wakusoku
import Xhamster_com
import lolig_blog
import sugumiru18_com
import HentaiHaven_org
import REDTUBE_com
import moeimg_net
import muchaero_net
import nijibondo_com
import nizigazo_net
import okkisokuho_com
import Pornhub_com


class DownloadList(object):
    """docstring for DownloadList"""
    def __init__(self, url, limit=None):
        super(DownloadList, self).__init__()
        self.fileStatus = self.getFileStatus(url, limit)

    def getFileStatus(self, url, limit=None):
        urlArray = self.splitURL(url)
        if urlArray[0] == 'dlbooks.to':
            print 'dropbooks'
            fileStatus = dropBOOKS_tv.run(url, urlArray, limit).filestatus
        elif urlArray[0] == 'www.xvideos.com':
            print 'xvideos'
            fileStatus = Xvideos_com.run(url, urlArray).filestatus
        elif urlArray[0] == 'animehaven.org' or urlArray[0] == 'animehaven.to':
            print 'animehaven'
            fileStatus = AnimeHaven_org.run(url, urlArray).filestatus
        elif urlArray[0] == 'hentaihaven.org':
            print 'hentaihaven'
            fileStatus = HentaiHaven_org.run(url, urlArray).filestatus
        elif urlArray[0] == 'blog.livedoor.jp':
            if urlArray[1] == 'wakusoku':
                print 'wakusoku'
                fileStatus = wakusoku.run(url, urlArray, limit).filestatus
        elif urlArray[0] == 'xhamster.com':
            print 'XHamster'
            fileStatus = Xhamster_com.run(url, urlArray).filestatus
        elif urlArray[0] == 'lolig.blog.jp':
            print 'lolig'
            fileStatus = lolig_blog.run(url, urlArray, limit).filestatus
        elif urlArray[0] == 'sugumiru18.com':
            print 'sugumiru18'
            fileStatus = sugumiru18_com.run(url, urlArray, limit).filestatus
        elif urlArray[0] == 'www.redtube.com':
            print 'REDTUBE'
            fileStatus = REDTUBE_com.run(url, urlArray).filestatus
        elif urlArray[0] == 'moeimg.net':
            print 'moeimg'
            fileStatus = moeimg_net.run(url, urlArray, limit).filestatus
        elif urlArray[0] == 'muchaero.net':
            print 'muchaero'
            fileStatus = muchaero_net.run(url, urlArray, limit).filestatus
        elif urlArray[0] == 'nizigazo.net':
            print 'nizigazo'
            fileStatus = nizigazo_net.run(url, urlArray, limit).filestatus
        elif urlArray[0] == 'nijibondo.com':
            print 'nijibondo'
            fileStatus = nijibondo_com.run(url, urlArray, limit).filestatus
        elif urlArray[0] == 'okkisokuho.com':
            print 'okkisokuho'
            fileStatus = okkisokuho_com.run(url, urlArray, limit).filestatus
        elif urlArray[0] == 'www.pornhub.com' or urlArray[0] == 'jp.pornhub.com':
            print 'pornhub'
            fileStatus = Pornhub_com.run(url, urlArray).filestatus
        return fileStatus

    def splitURL(self, url):
        url = url.replace('https', 'http')
        url = url.replace('http://', '')
        urlArray = url.split('/')
        return urlArray
