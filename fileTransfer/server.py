#!/usr/bin/env python3
# server
import socket
import sys
import os
from pathlib import Path
import uuid
import re

HOST = ''    # Symbolic name meaning all available interfaces
PORT = 12480 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

waitingForFiles = False
filename = ''

while(1):
    s.listen(1)
    # print type(s.accept())
    conn, addr = s.accept()

    print('Incoming Data from: ', addr)
    fileUid = uuid.uuid4().hex

    tst = open('tempDL/TempReceived-'+fileUid,'wb')
    while 1:
        data = conn.recv(1024)
        if data:
            tst.write(data)
        else:
            conn.close()
            tst.close()

            print('Transfer Complete.')
            dataString = open('tempDL/TempReceived-'+fileUid, errors='ignore').read()

            if not waitingForFiles:
                if dataString.startswith('error'):
                    if Path('tempDL/TempReceived-'+fileUid).is_file():
                        os.remove('tempDL/TempReceived-'+fileUid)
                    print('ERROR')

                elif dataString.startswith('NewFile'):
                    if Path('tempDL/TempReceived-'+fileUid).is_file():
                        os.remove('tempDL/TempReceived-'+fileUid)
                    print('-------------- '+dataString.split(',')[0]+' --------------')
                    print('Filename: '+dataString.split(',')[1].split('>')[1])
                    print('Parts: '+dataString.split(',')[2].split('>')[1])
                    filename = dataString.split(',')[1].split('>')[1]
                    waitingForFiles = True

                elif dataString.startswith('PartFile'):
                    if Path('tempDL/TempReceived-'+fileUid).is_file():
                        os.remove('tempDL/TempReceived-'+fileUid)
                    print('-------------- '+dataString.split(',')[0]+' --------------')
                    print('Filename: '+dataString.split(',')[1].split('>')[1])
                    filename = dataString.split(',')[1].split('>')[1]
                    waitingForFiles = True

                elif dataString.startswith('FileCompleted'):
                    regex = re.compile('[^a-zA-Z0-9]')
                    suffix = regex.sub('', dataString.split(',')[1].split('>')[1])
                    os.remove('cat *'+suffix+' > '+filename+'.mp4')
                    
                    
            else:
                os.rename('tempDL/TempReceived-'+fileUid, 'tempDL/'+filename)
                print('Synced: '+filename)
                waitingForFiles = False
            break