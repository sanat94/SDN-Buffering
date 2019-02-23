import socket
from time import sleep
from threading import Thread
import sys
import os
import subprocess



ffplayPID  = []
reconnected = True

def killProcesses():
    print('Killing processes')
    for pid in ffplayPID:
        pid.send_signal(1)

def connectStartFFMEG():
    print('Starting ffplay')
    args1 = ["ffplay","-probesize","32","-listen","1","rtmp://192.168.2.1:1234"]
    args2 = ["ffplay","-probesize","32","-listen","1","rtmp://192.168.2.1:1235"]
    args3 = ["ffplay","-probesize","32","-listen","1","rtmp://192.168.2.1:1236"]
    process1 = subprocess.Popen(args1, shell= False)
    process2 = subprocess.Popen(args2, shell= False)
    process3 = subprocess.Popen(args3, shell= False)
    ffplayPID.append(process1)
    ffplayPID.append(process2)
    ffplayPID.append(process3)


def startPlaying():
    while True:
        if reconnected:
            killProcesses()
            connectStartFFMEG()
            reconnected = False


def connectToSocket():
    clientSocket = socket.socket()
    host = '192.168.1.1'
    port = 25000
    clientSocket.connect((host,port))
    connected = True
    while True:

        try:
            print(host)
            clientSocket.send(bytes('Connected','UTF-8'))
        except socket.error:
            connected = False
            clientSocket = socket.socket()
            print('connection Lost...reconnecting')
            while not connected:
                try:
                    clientSocket.connect((host, port))
                    clientSocket.send(bytes('reconnected', 'UTF-8'))
                    reconnected = True
                    connected = True
                except socket.error:
                    sleep(0.5)


    clientSocket.close()


t = Thread(target=connectToSocket, args=())
t.start()
startPlaying()