# -*- coding: utf-8 -*-
import http.client
import importlib
import re
import sys
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from . import tiwi_kiwi
from ._helper import AccessPage

importlib.reload(sys)
SeqFlag = True


class Run(object):
    """docstring for Run"""
    def __init__(self, url, url_array):
        super(Run, self).__init__()
        self.urls = []
        # get type and soup
        st = SiteType(url_array)
        soup = SoupURL(url)
        urls = self.get_urls(st.type, soup.soup)
        self.file_status = {'urls': urls, 'dir': 'h_anime_place'}

    def get_urls(self, url_type, soup):
        if url_type == 'media':
            list_url = Media(soup).pref
        elif url_type == 'index':
            list_url = Index(soup).pref
        else:
            list_url = []
        return list_url


class SiteType(object):
    """docstring for SiteType"""
    def __init__(self, url_array):
        super(SiteType, self).__init__()
        self.type = self.get_type(url_array)

    def get_type(self, url_array):
        if 'episode' in url_array[1]:
            url_type = 'media'
        else:
            url_type = 'index'
        return url_type


class SoupURL(object):
    """docstring for SoupURL"""
    def __init__(self, url):
        super(SoupURL, self).__init__()
        self.soup = self.get_soup(url)

    def get_soup(self, url):
        x = AccessPage(url)
        soup = BeautifulSoup(x.html)
        return soup


# === Single Download ===
class Media(object):
    """docstring for Media"""
    def __init__(self, soup):
        super(Media, self).__init__()
        x = {}
        x['title'] = self.get_title(soup)
        # get download link
        x['href'] = self.get_file_url(soup)
        self.pref = [x]

    def get_title(self, soup):
        try:
            title = soup.title.string.split("|")[0].strip()
            title = re.sub(r'[^(\w\d\-\[\])]', '', title)
            title = re.sub(r'[/]', '_', title) + '.mp4'
            return title
        except:
            raise

    def get_file_url(self, soup):
        self.checkDL = False
        url = ''
        if not self.checkDL:
            url = self.get_url_from_dir(soup)
        if not self.checkDL:
            url = self.get_url_from_tiwikiwi(soup)
        return url

    def get_url_from_dir(self, soup):
        try:
            a_s = soup.findAll("a", attrs={"class": "btn btn-1 btn-1e"})
            url = a_s[0]['href'].encode("utf8")
            self.checkDL = True
            return url
        except:
            self.checkDL = False

    def expand_shorten_url(self, surl):
        parsed = urlparse(surl)
        h = http.client.HTTPConnection(parsed.netloc)
        h.request('HEAD', parsed.path)
        response = h.getresponse()
        if response.status / 100 == 3 and response.getheader('Location'):
            return response.getheader('Location')
        else:
            return surl

    def get_url_from_tiwikiwi(self, soup):
        try:
            short_url = soup.article.find(
                "a", attrs={"class": "btn btn-1 btn-1e"}
            )["href"]
            url = self.expand_shorten_url(short_url)
            url = AccessPage(url).html.url
            if 'tiwi.kiwi' in url:
                originurl = url
                url = url.replace('http://', '')
                url_array = url.split('/')
                site = tiwi_kiwi.Run(originurl, url_array)
                file_url = site.urls[0]['href'].encode("utf8")
                self.checkDL = True
                return file_url
        except:
            self.checkDL = False


# === List Download ===
class Index(object):
    """docstring for Index"""
    def __init__(self, soup):
        super(Index, self).__init__()
        self.pref = []
        urls = self.get_media_url(soup)
        for x in urls:
            try:
                l = {}
                soup = SoupURL(x).soup
                m = Media(soup)
                l['title'] = m.pref[0]['title']
                l['href'] = m.pref[0]['href'].encode("utf8")
                self.pref += [l]
            except:
                print('Error: ' + x)
            else:
                print(x)

    def get_media_url(self, soup):
        a_tag = soup.findAll("a", attrs={"class": "thumbnail-image"})
        media_url = []
        for x in a_tag:
            media_url += [x['href']]
        return media_url


# === test code ===
# url = 'http://hentaihaven.org/rance-01-the-quest-for-hikari-episode-1/'

# url = url.replace('https', 'http')
# aurl = url.replace('http://', '')
# url_array = aurl.split('/')

# x = Run(url, url_array)
# for media in x.urls:
#     print(media['title'])
#     print(media['href'])
#     print('')
