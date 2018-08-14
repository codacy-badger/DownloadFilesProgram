# -*- coding: utf-8 -*-
import urllib
import urllib3
import certifi
import re

from bs4 import BeautifulSoup

from selenium import webdriver


def get_limit_time(time_string):
    limit_day = time_string
    if limit_day is None:
        print('Till when?')
        print('ex. YYYY/MM/DD')
        limit_day = input('-> ')
    # check Str Type
    while True:
        LimitTime = limit_day
        limit_day = limit_day.replace(' ', '')
        limit_day = limit_day.replace('/', '')
        limit_day = limit_day.replace(':', '')
        limit_day += '0000'
        if len(limit_day) == 12:
            return int(limit_day)
        else:
            print('Oops!')
            limit_day = input('-> ')


def convert_url(url):
    regex = r'[^\x00-\x7F]'
    matchedList = re.findall(regex, url)
    for m in matchedList:
        url = url.replace(m, urllib.parse.quote_plus(m, encoding = "utf-8"))
    return url


def get_soup(url):
    x = AccessPage(url)
    soup = BeautifulSoup(x.html, "html.parser")
    return soup


class AccessPage(object):
    """docstring for AccessPage"""
    def __init__(self, url):
        super(AccessPage, self).__init__()
        self.html = self._get_html(url)

    def _get_html(self, url):
        if 'SEQUENCE' in url:
            return ''

        http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where())
        # set user
        headers = {
            'User-Agent':  'Mozilla/5.0'
        }
        url = convert_url(url)
        r = http.request('GET', url, headers=headers)
        # access page
        return r.data

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
