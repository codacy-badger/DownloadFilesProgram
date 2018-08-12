# -*- coding: utf-8 -*-
import socket
import subprocess
import sys
import urllib
import urllib3
import requests
from tqdm import tqdm


class DownloadFile(object):
    """docstring for DownloadFile"""
    def __init__(self, url, filename):
        super(DownloadFile, self).__init__()
        self.headers = {
            'User-Agent':  'Mozilla/5.0'
        }
        self.loopcnt = 0
        self.dlfile(url, filename)

    def dlfile(self, url, filename):
        if self.loopcnt > 3:
            try:
                cmd = 'wget "{}" -O "{}"'.format(url, filename)
                print('>> ' + cmd)
                subprocess.call(cmd, shell=True)
                raise requests.HTTPError('over 3times')
            except Exception as e:
                print(e)
                raise
        else:
            self.loopcnt += 1

        # Open the url
        try:
            r = requests.get(url, stream=True, headers=self.headers)
            total_size = int(r.headers['content-length'])
            chunk_size = 8192
            # Open our local file for writing
            with open(filename, "wb") as local_file:
                for data in tqdm(
                    iterable=r.iter_content(chunk_size=chunk_size),
                    total=total_size / chunk_size,
                    unit='KB'
                ):
                    local_file.write(data)
        # handle errors
        except requests.HTTPError as e:
            print("HTTP Error:", e.code, url)
            if not (self.loopcnt > 3):
                self.dlfile(url, filename)
            else:
                raise
        except socket.timeout as e:
            print("Timeout Error         ")
            self.dlfile(url, filename)
        except Exception as e:
            raise

        self.loopcnt = 0
