#!/usr/bin/python3
# -*- coding: utf-8 -*-
#SYN:xjanou06

import re
from error import Error


class Tag():
    beg = 0
    end = 0
    tag = ''

    def __init__(self, beg, end, tag):
        self.beg = int(beg)
        self.end = int(end)
        self.tag = str(tag)

    def getBegPos(self):
        return self.beg

    def getEndPos(self):
        return self.end

    def getTagName(self):
        return self.tag

    def __str__(self):
        return 'Beg: ' + str(self.getBegPos()) + ', End: ' + str(self.getEndPos()) + ', Name: ' + self.getTagName()
