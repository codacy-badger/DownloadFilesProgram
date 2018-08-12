# -*- coding: utf-8 -*-
import socket
import subprocess
import sys
import urllib


class DownloadFile(object):
    """docstring for DownloadFile"""
    def __init__(self, url, filename):
        super(DownloadFile, self).__init__()
        self.loopcnt = 0
        self.dlfile(url, filename)

    def chunk_read(self, response, chunk_size=8192, report_hook=None):
        total_size = response.info()['Content-Length'].strip()
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
                print('>> ' + cmd)
                subprocess.call(cmd, shell=True)
                raise urllib.error.HTTPError('over 3times')
            except Exception as e:
                print(e)
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
                "%.2f %% (%d MB)\r" % (percent, total_size / 1024 / 1024)
            )

            if bytes_so_far >= total_size:
                sys.stdout.write('\n')

            self.percentStack = percent
        # --------------------------

        # Open the url
        try:
            headers = {
                'User-Agent':  'Mozilla/5.0'
            }
            req = urllib.request.Request(url, None, headers)
            response = urllib.request.urlopen(req, timeout=5)
            data = self.chunk_read(
                response,
                report_hook=chunk_report)
            # Open our local file for writing
            with open(filename, "wb") as local_file:
                local_file.write(data)
        # handle errors
        except urllib.error.HTTPError as e:
            print("HTTP Error:", e.code, url)
            if not (self.loopcnt > 3):
                self.dlfile(url, filename)
            else:
                raise
        except urllib.error.URLError as e:
            print("URL Error:", e.reason, url)
            self.dlfile(url, filename)
        except socket.timeout as e:
            print("Timeout Error         ")
            self.dlfile(url, filename)
        except Exception as e:
            raise

        self.loopcnt = 0
