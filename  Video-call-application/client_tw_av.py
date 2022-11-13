import socket, sys, cv2, pickle, struct
from threading import Thread
from datetime import datetime
from time import sleep
import matplotlib.pyplot as plt
import numpy as np
import pyaudio

sending, receiving = False, False
HEADERSIZE = 10

class myClass:
    def __init__(self, name, img):
        self.threads = []
        self.stop = False
        self.name = name
        self.img = img
        self.local_buffer = None
        self.p = pyaudio.PyAudio() 
        self.stream = p.open(format=sample_format, channels=channels, rate=fs, frames_per_buffer=chunk, input=True, output=True)


    def send_to_client(self, clientsocket):
        cam = cv2.VideoCapture(0)
        cam.set(3, 320)
        cam.set(4, 240)
        img_counter = 0
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        while True:
            ret, frame = cam.read()
            try:
                result, frame = cv2.imencode('.jpg', frame, encode_param)
            except:
                continue
            data = pickle.dumps(frame, 0)
            size = len(data)
            if(self.stop):
                break
            else:
                clientsocket.sendall(bytes("{:<{}}".format(len(data), HEADERSIZE), 'utf-8') + data)
                img_counter += 1
                sleep(0.5)
        print("Client stop sending!")
        cam.release()


    def receive_from_client(self, clientsocket):
        print("Receiving...", receiving)
        while not self.stop:
            data = b""
            payload_size = HEADERSIZE
            msg_size = int(clientsocket.recv(HEADERSIZE))
            while len(data) < msg_size:
                data += clientsocket.recv(4096)
            frame_data = data # [:msg_size]
            if(len(frame_data)==0):
                continue
            frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

            cv2.imshow(self.name,frame)
            cv2.resizeWindow(str(clientsocket), 320, 240)
            cv2.waitKey(1)
        print("Receiving(stopped)...")
        cv2.destroyAllWindows()
                
    def fetchAudio(self, audio_socket):
       frames = []
       while not self.stop:
        try:
            print("getting audio....")
            data = audio_socket.recv(4096)
            #print("frames:", len(frames))
            frames.append(data)
            print(len(data))
            self.stream.write(data)     
        except:
          continue

    def recordAudio(self, audio_socket):  
      while not self.stop:
          data = self.stream.read(chunk)
          audio_socket.sendall(data)

    
    def inititate(self, clientsocket, audio_socket):
        t = Thread(target=self.send_to_client, args=(clientsocket, ))
        t2 = Thread(target=self.receive_from_client, args=(clientsocket, ))
        t3 = Thread(target=self.show_message, args=( ))
        
        audioSendingThread = Thread(target = self.recordAudio, args = (audio_socket,))
        audioReceivingThread = Thread(target = self.fetchAudio, args = (audio_socket,))
        
        self.stop = False
        while(len(self.threads)!=2):
            try:
                c = int(input("1: initiate sending \n 2: initiate receiving:"))
            except:
                continue
            if(c==1):
                t.start()
                audioReceivingThread.start()
                self.threads.append(t)
            elif(c==2):
                t2.start()
                audioSendingThread.start()
                self.threads.append(t2)

    def end(self):
        self.stop = True
        for t in self.threads:
            t.join()
        self.stream.close()
        self.p.terminate()



IP = "192.168.0.108"
PORT = 1234

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
seconds = 3



audio_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((IP, 1222))
audio_socket.connect((IP, PORT))

plt.show()
obj = myClass(name, img)
obj.inititate(s, audio_socket)
# input("Enter to stop")
input()
obj.end()
s.close()