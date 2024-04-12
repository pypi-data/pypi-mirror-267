#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2/14/2023 2:23 PM
# @Author  : zhangbc0315@outlook.com
# @File    : fast_numerous_file.py
# @Software: PyCharm

import os


class FastNumerousFile:

    def __init__(self, dp: str, max_file_in_dir: int = 1e3):
        self._info = {}
        self._info_fp = os.path.join(dp, '.info')
        self._fid = 0

    def add_file(self, file_name: str = None, file_suffix: str = None):
        file_name = str(self._fid) if file_name is None else file_name
        file_suffix = '' if file_suffix is None else '.' + file_suffix
        fn = file_name + file_suffix
        self._fid += 1

    def _dump_info(self):
        pass

    def _load_info(self):
        pass


if __name__ == "__main__":
    pass
