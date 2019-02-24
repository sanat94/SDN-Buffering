import socket
from time import sleep
from threading import Thread
import sys
import os
import subprocess


reconnected = True


ffplayPID  = []

def killProcesses():
    print('Killing processes')
    for pid in ffplayPID:
        pid.send_signal(1)

def connectStartFFMEG():
    print('Starting ffplay')
    args1 = ["ffplay","-probesize","32","-listen","1","rtmp://localhost:1935"]
    args2 = ["ffmpeg","-f","v4l2","-i","/dev/video0","-f","flv","rtmp://172.16.0.119:1234","-f","flv","rtmp://172.16.0.119:1235","-f","flv","rtmp://172.16.0.119:1236","-f","flv","rtmp://localhost:1935"]

    #args2 = ["ffmpeg","-f","v4l2","-i","/dev/video0","-f","flv","rtmp://localhost:1935"]
    process1 = subprocess.Popen(args1, shell= False)
    process2 = subprocess.Popen(args2, shell= False)
    ffplayPID.append(process1)
    ffplayPID.append(process2)


def startPlaying():
    global reconnected
    while True:
        if reconnected:
            killProcesses()
            connectStartFFMEG()
            reconnected = False



def connectToSocket():
    global reconnected
    serverSocket = socket.socket()
    host = '172.16.0.119'
    port = 25000
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)	
    serverSocket.bind( ( host, port ) )
    serverSocket.listen( 1 )

    con, addr = serverSocket.accept()

    print( "connected to client" )

    while True:
        message = con.recv(1024).decode("UTF-8")
        if message == 'reconnected':
            reconnected = True
        print(message)
        sleep(1)

    con.close();

try:
	t = Thread(target=connectToSocket, args=())
	t.start()
except KeyboardInterrupt:
        print("Ctrl-c pressed ...")
        sys.exit(1)
sleep(2)
startPlaying()
