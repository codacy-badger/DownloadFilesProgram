# -*- coding: utf-8 -*-
import urllib

from bs4 import BeautifulSoup

from selenium import webdriver


class AccessPage(object):
    """docstring for AccessPage"""
    def __init__(self, url, browser=False):
        super(AccessPage, self).__init__()
        self.html = ''
        if browser:
            self.html, self.driver = self.get_html_by_browser(url)
        else:
            self.html = self.get_html(url)

    def get_html(self, url):
        if 'SEQUENCE' in url:
            return ''
        try:
            # set user
            user_agent = 'Mozilla/5.0'
            # user_agent = 'Chrome/41.0.2228.0'
            req = urllib.Request(url)
            req.add_header("User-agent", user_agent)
            # access page
            return urllib.urlopen(req)
        except:
            raise

    def get_html_by_browser(self, url):
        if 'SEQUENCE' in url:
            return ''

        # Selenium settings
        driver = webdriver.PhantomJS()
        # get a HTML response
        driver.get(url)
        html = driver.page_source.encode('utf-8')
        # access page
        return html, driver


class SoupURL(object):
    """docstring for SoupURL"""
    def __init__(self, url):
        super(SoupURL, self).__init__()
        self.s = self.get_soup(url)

    def get_soup(self, url):
        # print(url)
        x = AccessPage(url)
        soup = BeautifulSoup(x.content, 'html.parser')
        return soup
