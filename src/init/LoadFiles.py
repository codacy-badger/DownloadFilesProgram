# -*- coding: utf-8 -*-
import json
import os
import sys


# load setting.json
class LoadSetting(object):
    """docstring for LoadSetting"""
    def __init__(self, json_file):
        super(LoadSetting, self).__init__()
        self.setting = self.load(json_file)

    def load(self, json_file):
        # fix path
        json_file = os.path.expanduser(json_file)
        # open json file
        try:
            with open(json_file, 'r') as f:
                x = json.load(f)
        except:
            print("設定ファイルが開けません")
            sys.exit()
        # fix paths
        for k, v in x.items():
            x[k] = os.path.expanduser(v)
        return x
