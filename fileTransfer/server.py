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
fileCurrentlyProcessing = ''

while(1):
    s.listen(1)
    # print type(s.accept())
    conn, addr = s.accept()

    print('Incoming Data from: ', addr)
    fileUid = uuid.uuid4().hex

    tst = open('temp/TempReceived-'+fileUid,'wb')
    while 1:
        data = conn.recv(1024)
        if data:
            tst.write(data)
        else:
            conn.close()
            tst.close()

            print('Transfer Complete.')
            dataString = open('temp/TempReceived-'+fileUid, errors='ignore').read()

            if not waitingForFiles:
                if dataString.startswith('error'):
                    if Path('temp/TempReceived-'+fileUid).is_file():
                        os.remove('temp/TempReceived-'+fileUid)
                    print('ERROR')
                elif dataString.startswith('NewFile'):
                    if Path('temp/TempReceived-'+fileUid).is_file():
                        os.remove('temp/TempReceived-'+fileUid)
                    print('-------------- '+dataString.split(',')[0]+' --------------')
                    print('Filename: '+dataString.split(',')[1].split('>')[1])
                    print('Parts: '+dataString.split(',')[2].split('>')[1])
                    waitingForFiles = True
                    partsInQueue = int(dataString.split(',')[2].split('>')[1])
            else:
                filename = dataString.split(':')[-1]
                if Path('filename').is_file():
                    os.remove(filename)
                os.rename('temp/TempReceived-'+fileUid, filename)
                print('Synced: '+filename)
            break