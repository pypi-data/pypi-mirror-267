#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 4/12/2024 11:13 AM
# @Author  : zhangbc0315@outlook.com
# @File    : fast_math.py
# @Software: PyCharm

import numpy as np


class FastMath:

    @classmethod
    def lorentzian(cls, xs, x0, gamma):
        return 1 / (np.pi * gamma * (1 + ((xs - x0) / gamma) ** 2))


if __name__ == "__main__":
    pass
