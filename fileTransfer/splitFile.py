#!/usr/bin/env python3

import sys
import os
import re

def splitFileIntoParts(fileToSplit, fileName):
    print('Spliting File...')
    regex = re.compile('[^a-zA-Z0-9]')
    suffix = regex.sub('', fileName)
    os.system('split -b 100000000 \''+fileToSplit+'\' tempUL/  --additional-suffix='+suffix)