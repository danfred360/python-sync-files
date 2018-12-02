#!/usr/bin/env python3
# server
import socket
import sys
import os
from pathlib import Path
import uuid
import re
from time import sleep

HOST = ''    # Symbolic name meaning all available interfaces
PORT = 12480 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

waitingForFiles = False
filename = ''
fullfilename = ''

bandwidthKB = 5000
bandwidthDelay = (1/bandwidthKB)

while(1):
    s.listen(1)
    # print type(s.accept())
    conn, addr = s.accept()

    print('Incoming Data from: ', addr)
    fileUid = uuid.uuid4().hex

    tst = open('tempDL/TempReceived-'+fileUid,'wb')
    while 1:
        data = conn.recv(1024)
        sleep(bandwidthDelay)
        if data:
            tst.write(data)
        else:
            conn.close()
            tst.close()

            print('Transfer Complete: '+str(os.path.getsize('tempDL/TempReceived-'+fileUid) >> 20))
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
                    print('\n')
                    filename = dataString.split(',')[1].split('>')[1]
                    fullfilename = filename

                elif dataString.startswith('PartFile'):
                    if Path('tempDL/TempReceived-'+fileUid).is_file():
                        os.remove('tempDL/TempReceived-'+fileUid)
                    print('-------------- '+dataString.split(',')[0]+' --------------')
                    print('Filename: '+dataString.split(',')[1].split('>')[1])
                    filename = dataString.split(',')[1].split('>')[1]
                    waitingForFiles = True

                elif dataString.startswith('FileCompleted'):
                    if Path('tempDL/TempReceived-'+fileUid).is_file():
                        os.remove('tempDL/TempReceived-'+fileUid)
                    regex = re.compile('[^a-zA-Z0-9]')
                    suffix = regex.sub('', dataString.split(',')[1].split('>')[1])
                    os.system('cat tempDL/*'+suffix+' > \''+fullfilename+'\'')
                    print('-------------- '+dataString.split(',')[0]+' --------------')
                    os.system('rm tempDL/*'+suffix)
                        
            else:
                os.rename('tempDL/TempReceived-'+fileUid, 'tempDL/'+filename)
                print('Synced: '+filename)
                print('\n')
                waitingForFiles = False
            break