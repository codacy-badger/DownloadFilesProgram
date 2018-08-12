# -*- coding: utf-8 -*-
import re
import time

from bs4 import BeautifulSoup

from .AccessSite.OpenHTML import AccessPage


class Run(object):
    """docstring for Run"""
    def __init__(self, url, url_array):
        super(Run, self).__init__()
        self.urls = []
        # get type and soup
        st = SiteType(url_array)
        soup = SoupURL(url)
        urls = self.get_urls(st.type, soup.s)
        # self.urls = urls
        self.file_status = {'urls': urls, 'dir': 'h_video_place'}

    def get_urls(self, url_type, soup):
        if url_type == 'media':
            list_url = Media(soup).pref
        else:
            list_url = []
        return list_url


class SiteType(object):
    """docstring for SiteType"""
    def __init__(self, url_array):
        super(SiteType, self).__init__()
        self.type = self.get_type(url_array)

    def get_type(self, url_array):
        if 'video' in url_array[1]:
            url_type = 'media'   # media url
        else:
            url_type = None
        return url_type


class SoupURL(object):
    """docstring for SoupURL"""
    def __init__(self, url):
        super(SoupURL, self).__init__()
        self.s = self.get_soup(url)

    def get_soup(self, url):
        x = AccessPage(url)
        soup = BeautifulSoup(x.html)
        return soup


class Media(object):
    """docstring for Media"""
    def __init__(self, soup):
        super(Media, self).__init__()
        x = {}
        x['title'] = self.get_title(soup)
        x['href'] = self.get_file_url(soup)
        self.pref = [x]

    def get_title(self, soup):
        title_str = soup.title.string
        title = title_str.split("- Pornhub.com")[0].split("(")[0].strip()
        title = re.sub(r'[^(\w\d\-\[\])]', '', title)
        if len(title) == 0:
            title = 'ut' + str(int(time.time()))
        title = title + '.mp4'
        return title

    def get_file_url(self, soup):
        try:
            js = soup.find('div', attrs={'id': 'player'})
            scr = js.find('script')
            scr_string = scr.string

            # pattern = r'\"https:\/\/.+\.mp4.+\"'
            pattern = re.compile(
                r'(?<="videoUrl":")https:\\/\\/.+\.mp4.+?(?="})')
            m = pattern.search(scr_string, re.DOTALL).group(0)
            media_url = m.split('"')[0]
            media_url = media_url.replace('\/', '/')
            return media_url
        except:
            raise


# === test code ===
# url = 'https://www.pornhub.com/view_video.php?viewkey=730950062'

# url = url.replace('https', 'http')
# aurl = url.replace('http://', '')
# url_array = aurl.split('/')

# x = Run(url, url_array)
# print(x.urls)
# for media in x.urls:
#     print(media['title'])
#     print(media['href'])
#     print('')
