#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import socket
import urllib
import urllib2
import subprocess


class DownloadFile(object):
    """docstring for DownloadFile"""
    def __init__(self, url, filename):
        super(DownloadFile, self).__init__()
        self.loopcnt = 0
        self.dlfile(url, filename)

    def chunk_read(self, response, chunk_size=8192, report_hook=None):
        total_size = response.info().getheader('Content-Length').strip()
        total_size = int(total_size)
        bytes_so_far = 0
        data = []

        while 1:
            try:
                chunk = response.read(chunk_size)
            except:
                raise
            bytes_so_far += len(chunk)

            if not chunk:
                break

            data += chunk
            if report_hook:
                report_hook(bytes_so_far, chunk_size, total_size)

        return "".join(data)

    def dlfile(self, url, filename):
        if self.loopcnt > 3:
            try:
                cmd = 'wget "{}" -O "{}"'.format(url, filename)
                print '>> ' + cmd
                subprocess.call(cmd, shell=True)
                raise urllib2.HTTPError('over 3times')
            except Exception as e:
                print e
                raise
        else:
            self.loopcnt += 1

        # --- progress function ---
        def chunk_report(bytes_so_far, chunk_size, total_size):
            percent = float(bytes_so_far) / total_size
            percent = round(percent * 100, 2)
            # sys.stdout.write(
            #     "Downloaded %d of %d bytes (%0.2f%%)\r" %
            #     (bytes_so_far, total_size, percent)
            # )
            sys.stdout.write(
                "%.2f %% (%d MB)\r" % (percent, total_size/1024/1024)
            )

            if bytes_so_far >= total_size:
                sys.stdout.write('\n')

            self.percentStack = percent
        # --------------------------

        # Open the url
        try:
            user_agent = 'Mozilla/5.0'
            # user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.63 Safari/537.36'
            # user_agent = 'Wget/1.9.1'
            req = urllib2.Request(str(url))
            req.add_header("User-agent", user_agent)
            response = urllib2.urlopen(req, timeout=5)
            data = self.chunk_read(
                response,
                report_hook=chunk_report)
            # Open our local file for writing
            with open(filename, "wb") as local_file:
                local_file.write(data)
        # handle errors
        except urllib2.HTTPError, e:
            print "HTTP Error:", e.code, url
            if not (self.loopcnt > 3):
                self.dlfile(url, filename)
            else:
                raise
        except urllib2.URLError, e:
            print "URL Error:", e.reason, url
            self.dlfile(url, filename)
        except socket.timeout, e:
            print "Timeout Error         "
            self.dlfile(url, filename)
        except Exception as e:
            raise

        self.loopcnt = 0
