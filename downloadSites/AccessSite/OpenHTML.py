#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- coding: cp932 -*-

import os
import sys
import json
from selenium import webdriver
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

    def getHTML_byPhantomjs(self, url):
        if 'SEQUENCE' in url:
            return ''

        # Selenium settings
        driver = webdriver.PhantomJS()
        # get a HTML response
        driver.get(url)
        html = driver.page_source.encode('utf-8')
        # access page
        return html


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
