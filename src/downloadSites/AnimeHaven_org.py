# -*- coding: utf-8 -*-
import re

from bs4 import BeautifulSoup

from . import tiwi_kiwi
from .OpenHTML import AccessPage


SeqFlag = True


class Run(object):
    """docstring for Run"""
    def __init__(self, url, url_array):
        super(Run, self).__init__()
        self.urls = []
        # get type and data
        st = SiteType(url_array)
        data = DataHTML(url)
        urls = self.get_urls(st.type, data)
        self.file_status = {'urls': urls, 'dir': 'anime_place'}

    def get_urls(self, url_type, data):
        if url_type == 'media':
            list_url = Media(data).pref
        elif url_type == 'index':
            list_url = Index(data).pref
        else:
            list_url = []
        return list_url


class SiteType(object):
    """docstring for SiteType"""
    def __init__(self, url_array):
        super(SiteType, self).__init__()
        self.type = self.get_type(url_array)

    def get_type(self, url_array):
        if url_array[1] == 'subbed' or url_array[1] == 'dubbed':
            url_type = 'media'
        elif url_array[1] == 'episodes':
            url_type = 'index'
        else:
            url_type = None
        return url_type


class DataHTML(object):
    """docstring for DataHTML"""
    def __init__(self, url):
        super(DataHTML, self).__init__()
        x = AccessPage(url, browser=True)
        self.soup = self.get_soup(x)
        self.driver = self.get_driver(x)

    def get_soup(self, x):
        soup = BeautifulSoup(x.html)
        return soup

    def get_driver(self, x):
        driver = x.driver
        return driver


# === Single Download ===
class Media(object):
    """docstring for Media"""
    def __init__(self, data):
        super(Media, self).__init__()
        x = {}
        x['title'] = self.get_title(data.soup)
        # get download link
        x['href'] = self.get_file_url(data)
        self.pref = [x]

    def get_title(self, soup):
        try:
            title = soup.title.string.split("|")[0].strip()
            title = re.sub(r'[/]', '_', title) + '.mp4'
            title = title
            return title
        except:
            raise

    def get_file_url(self, data):
        self.checkDL = False
        soup = data.soup
        url = ''
        if not self.checkDL:
            url = self.get_url_from_streammoe(data)
        if not self.checkDL:
            url = self.get_url_fromdownload_link(soup)
        if not self.checkDL:
            url = self.get_url_from_dir(soup)
        if not self.checkDL:
            url = self.get_url_from_tiwikiwi(soup)
        return url

    def get_url_from_tiwikiwi(self, soup):
        try:
            download_link = soup.find(
                'div',
                attrs={'class': 'download_feed_link'}
            ).a['href']
            if 'google' in download_link:
                self.checkDL = True
                return download_link
            url = download_link.replace('http://', '')
            url_array = url.split('/')
            site = tiwi_kiwi.Run(download_link, url_array)
            file_url = site.urls[0]['href'].encode("utf8")
            self.checkDL = True
            return file_url
        except:
            self.checkDL = False

    def get_url_from_streammoe(self, data):
        driver = data.driver
        try:
            iframes = driver.find_elements_by_tag_name('iframe')
            driver.switch_to.frame(iframes[2])
            iframes = driver.find_elements_by_tag_name('iframe')
            driver.switch_to.frame(iframes[0])

            html = driver.page_source.encode('utf-8')
            soup = BeautifulSoup(html)
            video = soup.find('video')
            file_url = video.source['src']

            self.checkDL = True
            return file_url
        except:
            self.checkDL = False

    def get_url_fromdownload_link(self, soup):
        try:
            a_s = soup.findAll('a', attrs={'class': 'download-btn-inline'})
            file_url = a_s[0]['href'].encode("utf8")
            self.checkDL = True
            return file_url
        except:
            self.checkDL = False

    def get_url_from_dir(self, soup):
        try:
            video = soup.find('video')
            sources = video.findAll('source')

            file_url = sources[0]['src'].encode("utf8")
            self.checkDL = True
            return file_url
        except:
            self.checkDL = False


# === List Download ===
class Index(object):
    """docstring for Index"""
    def __init__(self, data):
        super(Index, self).__init__()
        self.pref = []
        urls = self.get_media_url(data.soup)
        for x in urls:
            try:
                l = {}
                data = DataHTML(x)
                m = Media(data)
                l['title'] = m.pref[0]['title']
                l['href'] = m.pref[0]['href'].encode("utf8")
                self.pref += [l]
            except:
                print('Error: ' + x)
            else:
                print(x)

    def get_media_url(self, soup):
        tag_h2 = soup.findAll('h2', attrs={'class': 'entry-title'})
        media_url = []
        for x in tag_h2:
            media_url += [x.a['href']]
        return media_url


# === test code ===
# url = 'http://animehaven.org/subbed/one-punch-man-episode-7'

# url = url.replace('https', 'http')
# aurl = url.replace('http://', '')
# url_array = aurl.split('/')

# x = Run(url, url_array)
# for media in x.urls:
#     print(media['title'])
#     print(media['href'])
#     print('')
