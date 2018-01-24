#!/usr/bin/python
# -*- coding: cp949 -*-

import os

# get environ using key
s = os.environ['PATH']
print s
print 

# get all environ

keys = os.environ.keys()
keys.sort()

for key in keys:
    print "%s=%s" % (key, os.environ[key])
