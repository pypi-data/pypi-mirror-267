#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2022/10/9 17:09
# @File           : tools.py
# @IDE            : PyCharm
# @desc           : 工具类
import random
import string


def generate_string(length: int = 8) -> str:
    """
    生成随机字符串
    :param length: 字符串长度
    """
    return ''.join(random.sample(string.ascii_letters + string.digits, length))