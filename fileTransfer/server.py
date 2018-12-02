#!/usr/bin/env python3
# server
import socket
import sys
import os
from pathlib import Path
import uuid

HOST = ''    # Symbolic name meaning all available interfaces
PORT = 12480 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

waitingForFiles = False
partsInQueue = 0

while(1):
    s.listen(1)
    # print type(s.accept())
    conn, addr = s.accept()

    print('Incoming Data from: ', addr)
    fileUid = uuid.uuid4().hex

    tst = open('TempReceived-'+fileUid,'wb')
    while 1:
        data = conn.recv(1024)
        if data:
            tst.write(data)
        else:
            conn.close()
            tst.close()

            print('Transfer Complete.')
            linestring = open('TempReceived-'+fileUid, errors='ignore').read()

            if linestring.startswith('NewFile'):
                if Path('TempReceived-'+fileUid).is_file():
                    os.remove('TempReceived-'+fileUid)
                print(linestring)
            else:
                filename = linestring.split(':')[-1]
                if Path('filename').is_file():
                    os.remove(filename)
                os.rename('TempReceived-'+fileUid, filename)
                print('Synced: '+filename)
            break