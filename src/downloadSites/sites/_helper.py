# -*- coding: utf-8 -*-
import urllib
import urllib3
import certifi
import re

from bs4 import BeautifulSoup

from selenium import webdriver


def convert_url(url):
    regex = r'[^\x00-\x7F]'
    matchedList = re.findall(regex, url)
    for m in matchedList:
        url = url.replace(m, urllib.parse.quote_plus(m, encoding = "utf-8"))
    print(url)
    return url


class AccessPage(object):
    """docstring for AccessPage"""
    def __init__(self, url):
        super(AccessPage, self).__init__()
        self.html = self._get_html(url)

    def _get_html(self, url):
        if 'SEQUENCE' in url:
            return ''
        try:
            http = urllib3.PoolManager(
                cert_reqs='CERT_REQUIRED',
                ca_certs=certifi.where())
            # set user
            headers = {
                'User-Agent':  'Mozilla/5.0'
            }
            r = http.request('GET', url, headers=headers)
            # access page
            return r.data
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
