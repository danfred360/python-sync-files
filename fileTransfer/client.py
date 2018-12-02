#!/usr/bin/env python3
# client
import socket
import sys
 
HOST  = '10.0.0.200' # The target IP address
PORT  = 12480 # The target port as used by the server
DATA  = open('program.exe','r')
BDATA = DATA.read()
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
s.connect((HOST, PORT))
s.send(BDATA+':'+DATA.name) #Put the pattern you want to send here.
s.close()