import socket
import sys
import os
import time

def sendFileToServer(fileToSend, fileName, HOST, PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    DATA = 'PartFile,filename>'+fileName
    s.send(DATA) #Put the pattern you want to send here.
    s.close()

    DATA  = open(fileToSend,'r')
    BDATA = DATA.read()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send(BDATA) #Put the pattern you want to send here.
    s.close()
    return True