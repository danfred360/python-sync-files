#!/usr/bin/env python3
# client
import socket
import sys
import math
import os
import argparse
import ntpath
import re

import sendFile
import splitFile

parser = argparse.ArgumentParser()
parser.add_argument("path", type=str, help="Path of file to transfer")
parser.add_argument("-n", "--newfile", help="New File",action="store_true")
args = parser.parse_args()

fileLocation = args.path
print(fileLocation)

fileParts = str(int(math.ceil(os.path.getsize(fileLocation)/float(100000000))))
fileName = ntpath.basename(fileLocation)

HOST = '10.0.0.200' # The target IP address
PORT = 12480 # The target port as used by the server
DATA = 'error'
if args.newfile:
    DATA = 'NewFile,filename>'+fileName+',parts>'+fileParts
    splitFile.splitFileIntoParts(fileLocation, fileName)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print('Sending Data...')
s.send(DATA) #Put the pattern you want to send here.
s.close()

regex = re.compile('[^a-zA-Z0-9]')

if args.newfile:
    for files in os.listdir('tempUL/'):
        if files.endswith(regex.sub('', fileName)):
            print(files)
            sendFile.sendFileToServer('tempUL/'+files, files, HOST, PORT)
    print('------------------- All Data Transmitted -------------------')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    DATA = 'FileCompleted,filename>'+fileName+',parts>'+fileParts
    s.send(DATA) #Put the pattern you want to send here.
    s.close()
