import socket, sys, cv2, pickle, struct
from threading import Thread
from datetime import datetime
from time import sleep
import pyaudio
from array import array

sending, receiving = False, False
HEADERSIZE = 10
chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
seconds = 3

class myClass:
    def __init__(self, i, clientsocket, audiosocket):
        self.i = i
        self.name = str(i)
        self.threads = []
        self.stop = False
        self.buffer = None
        self.clientsocket = clientsocket
        self.audiosocket = audiosocket
        self.p = pyaudio.PyAudio() 
        self.stream = self.p.open(format=sample_format, channels=channels, rate=fs, frames_per_buffer=chunk, input=True, output=True)

    def receive_and_send(self, clientsocket, audiosocket):
        print("Receiving...", self.stop)
        while not self.stop:
            data = b""
            msg_size = int(clientsocket.recv(HEADERSIZE))
            # print(msg_size)
            while len(data) < msg_size:
                data += clientsocket.recv(4096)
            audio_data = audiosocket.recv(4096)

            ##############  send as soon as you receive it  #############
            o = 1 if(self.i==0) else 0
            clients[o].clientsocket.sendall(bytes("{:<{}}".format(len(data), HEADERSIZE), 'utf-8') + data)
            if(len(audio_data)==4096):
                print("S", end=" | ")

                self.stream.write(audio_data)
                print(max(array("h", audio_data)))
                clients[o].audiosocket.sendall(audio_data)
            ##############################################################
        print("Receiving(stopped)...", self.stop)
    
    def inititate(self):
        clientsocket, audiosocket = self.clientsocket, self.audiosocket

        t = Thread(target=self.receive_and_send, args=(clientsocket, audiosocket, ))
        self.stop = False
        t.start()
        sleep(1)
        self.threads.append(t)

    def end(self):
        self.stop = True
        self.clientsocket.close()
        for t in self.threads:
            t.join()
        self.stream.close()
        self.p.terminate()

IP = "192.168.0.108"
audio_PORT = 1234


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, 1222))
s.listen()

audio_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
audio_s.bind((IP, audio_PORT))
audio_s.listen()

clients = []
for i in range(2):
    print(i)
    clientsocket, addr = s.accept()
    audiosocket, addr =  audio_s.accept()
    obj = myClass(i, clientsocket, audiosocket)
    clients.append(obj)

clients[0].inititate()
clients[1].inititate()

#sleep(10)
input()
print("closing all")
for obj in clients:
    obj.end()
    