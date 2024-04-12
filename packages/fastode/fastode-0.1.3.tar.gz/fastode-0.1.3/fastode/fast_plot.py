#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 4/12/2024 10:51 AM
# @Author  : zhangbc0315@outlook.com
# @File    : fast_plot.py
# @Software: PyCharm


class FastPlot:

    @classmethod
    def split_bar(cls, nums, num_bar, min_num=None, max_num=None):
        if min_num is None:
            min_num = min(nums)
        if max_num is None:
            max_num = max(nums)
        gap = (max_num - min_num) / num_bar
        bars = []
        for i in range(num_bar):
            bars.append([min_num + i * gap, min_num + (i + 1) * gap])
        return bars


if __name__ == "__main__":
    pass
