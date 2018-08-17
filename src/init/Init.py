# -*- coding: utf-8 -*-
from . import LoadFiles
from . import PathCheck


class INIT(object):
    """docstring for INIT"""
    def __init__(self, setting):
        super(INIT, self).__init__()
        # value
        self.pref = None
        # get value
        self.get_setting(setting)
        self.check_dirs(self.pref)

    def get_setting(self, setting):
        self.pref = LoadFiles.LoadSetting(setting).setting

    def check_dirs(self, mix_dict):
        # get dirs
        dirs = []
        for k, v in mix_dict.items():
            if v[-1] == '/':
                dirs += [v]
        # check dirs
        PathCheck.CheckDirectory(dirs)
