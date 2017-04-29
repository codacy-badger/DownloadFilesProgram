#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- coding: cp932 -*-

import urllib2
from BeautifulSoup import BeautifulSoup


class AccessPage(object):
    """docstring for AccessPage"""
    def __init__(self, url):
        super(AccessPage, self).__init__()
        self.html = ''
        self.html = self.getHTML(url)

    def getHTML(self, url):
        if 'SEQUENCE' in url:
            return ''
        try:
            # set user
            user_agent = 'Mozilla/5.0'
            # user_agent = 'Chrome/41.0.2228.0'
            req = urllib2.Request(url)
            req.add_header("User-agent", user_agent)
            # access page
            return urllib2.urlopen(req)
        except:
            raise


class SoupURL(object):
    """docstring for SoupURL"""
    def __init__(self, url):
        super(SoupURL, self).__init__()
        self.s = self.getSoup(url)

    def getSoup(self, url):
        # print url
        x = AccessPage(url)
        soup = BeautifulSoup(x.html)
        return soup
