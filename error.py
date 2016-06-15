#!/usr/bin/python3
# -*- coding: utf-8 -*-
#SYN:xjanou06

import sys

PARAM_ERROR = 1
INPUT_ERROR = 2
OUTPUT_ERROR = 3
FORMAT_ERROR = 4


class Error():
    def paramError():
        sys.stderr.write('Invalid argument\n')
        exit(PARAM_ERROR)

    def inputError():
        sys.stderr.write('Invalid input file\n')
        exit(INPUT_ERROR)

    def outputError():
        sys.stderr.write('Invalid output file\n')
        exit(OUTPUT_ERROR)

    def formatError():
        sys.stderr.write('Invalid format\n')
        exit(FORMAT_ERROR)
