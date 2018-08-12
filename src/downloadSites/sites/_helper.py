# -*- coding: utf-8 -*-
import urllib

from bs4 import BeautifulSoup

from selenium import webdriver


class AccessPage(object):
    """docstring for AccessPage"""
    def __init__(self, url):
        super(AccessPage, self).__init__()
        self.html = ''
        self.html = self.get_html(url)

    def get_html(self, url):
        if 'SEQUENCE' in url:
            return ''
        try:
            # set user
            headers = {
                'User-Agent':  'Mozilla/5.0'
            }
            req = urllib.request.Request(url, None, headers)
            # access page
            return urllib.request.urlopen(req)
        except:
            raise

    def get_html_by_phantomjs(self, url):
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
        self.s = self.get_soup(url)

    def get_soup(self, url):
        # print url
        x = AccessPage(url)
        soup = BeautifulSoup(x.html, "html.parser")
        return soup
