'''
Authors: Daniel Frederick and Evan Trowbridge
Date: 12-1-2018
---------------------------------------------
TO DO -
-
Ports 12480 - 12481
'''

import os
import time

class sync:
    def __init__(self, path1, path2):
        self.dir1 = os.listdir(path1)
        self.dir2 = os.listdir(path2)

    def __str__(self):
        return 'Directory 1:\n{} \nDirectory 2:\n{}'.format(self.dir1, self.dir2)

temp = sync()