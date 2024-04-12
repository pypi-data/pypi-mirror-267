#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# File          : test1
# Author        : Sun YiFan-Movoid
# Time          : 2024/4/7 22:19
# Description   : 
"""
import time

from movoid_threading.thread import ThreadLib

mt = ThreadLib()


def test1():
    for i in range(10):
        print(f'test1 {i}')
        time.sleep(0.5)


def test2():
    for i in range(15):
        print(f'test2 {i}')
        time.sleep(0.2)


mt.new(test1)
for i1 in range(10):
    print(mt['Thread-1'].ident)
time.sleep(2)
mt['Thread-1'].force_stop()
time.sleep(0.2)
print(dict(mt))
