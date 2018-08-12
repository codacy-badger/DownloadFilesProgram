#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import glob
import os
import sys

from downloadSites.site_branch import DownloadList

from downloadfile import DownloadFile

from fileLog.codec import Codec
from fileLog.main import URLlog

from init.Init import INIT


parser = argparse.ArgumentParser(description='')
parser.add_argument('--limit', '-l', default=None)
args = parser.parse_args()


class Download(object):
    """docstring for Download"""
    def __init__(self, url, path, logdir):
        super(Download, self).__init__()
        self.dl(url, path, logdir)

    def dl(self, url, path, logdir):
        # --- progress function ---
        def _progress(block_count, block_size, total_size):
            percentage = 100.0 * block_count * block_size / total_size
            sys.stdout.write(
                "%.2f %% (%d KB)\r" % (percentage, total_size / 1024)
            )
        # --------------------------
        path = os.path.expanduser(path)
        self.check_dir(path)

        url = Codec().to_utf8(url)
        path = Codec().to_utf8(path)
        check_log = URLlog(logdir, url).check_log()

        try:
            if os.path.exists(path) or check_log:
                print('PASS : file already exist.')
                return
            # with urllib
            # urllib.urlretrieve(
            #     url,
            #     path,
            #     _progress
            # )
            DownloadFile(url, path)
        except:
            raise
        else:
            URLlog(logdir, url).check_log(addURL=True)

    def check_dir(self, path):
        array = path.split('/')
        last = array[-1]
        if '.' in last:
            del array[-1]
        dirpath = os.path.expanduser('/'.join(array))
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)


class LetsDownload(object):
    """docstring for LetsDownload"""
    def __init__(self, **arguments):
        super(LetsDownload, self).__init__()
        for media in arguments['urls']:
            self.parentDir = arguments['parentDir']
            filename = os.path.join(self.parentDir, media['title'])
            self.missFiles = []

            try:
                print("Start Download " + media['title'] + " !!")
                Download(media['href'], filename, self.parentDir)
            except Exception as e:
                self.missFiles += [media]
                print('Error DL : ' + str(e))
                print('Miss!!\n')
            else:
                print('Finish Download!!\n')

    def get_dir(self, title, **setting):
        ex = title[-4:]
        if ex == '.zip':
            return setting['zip_place']
        if ex == '.mp4' or ex == '.flv':
            return setting['mp4_place']
        if ex == '.jpg':
            return setting['jpg_place']


# === MAIN ===
def main():
    # title call
    print("")
    print("\n--------------------\n")
    print("  Let's DOWNLOAD!!!")
    print("\n--------------------\n")
    print("")

    # get place of URL list file
    set_place = '../setting.json'
    while True:
        try:
            setting = INIT(set_place)
            break
        except:
            set_place = input("Where setting.json? : ")
            set_place = os.path.expanduser(set_place)

    # get urls
    with open(setting.pref['urls_place'], 'r') as f:
        urls = f.readlines()

    # download
    print('')
    for url in urls:
        url = url.strip()

        x = DownloadList(url, args.limit)
        arguments = setting.pref
        arguments = x.file_status
        arguments.update({
            'parentDir': setting.pref[x.file_status['dir']],
        })
        LetsDownload(**arguments)

    # clean dirs
    print('\nClean Directorys...\n')
    dirs = glob.glob(setting.pref['h_pic_place'] + '*/')
    for i in dirs:
        i = i.replace(u'[ナルト-NARUTO]', '')
        if len(glob.glob(i + '*')) == 0:
            try:
                os.removedirs(i)
                print(i)
            except:
                pass

    print('\nFINISH!!\n')


if __name__ == "__main__":
    main()
    sys.exit()
