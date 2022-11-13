from __future__ import division
from flask import Flask
import os
import re
import sys
from flask import render_template
from flask_sockets import Sockets
import json
import threading
from six.moves import queue
from google.cloud import speech
from google.cloud.speech_v1 import types
import os
import base64
import logging
import pyaudio

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./credentials.json"


app = Flask(__name__)
sockets = Sockets(app)


@app.route('/')
def hello():    
    return render_template('index.html')


HTTP_SERVER_PORT = 8000
RATE = 16000
CHUNK = int(RATE / 10)

class Transcoder(object):
    """
    Converts audio chunks to text
    """
    def __init__(self, encoding, rate, language):
        self.buff = queue.Queue()
        self.encoding = encoding
        self.language = language
        self.rate = rate
        self.closed = True
        self.transcript = None

    def start(self):
        """Start up streaming speech call"""
        threading.Thread(target=self.process).start()

    def response_loop(self, responses):
        """
        Pick up the final result of Speech to text conversion
        """
        # for response in responses:
        #     if not response.results:
        #         continue
        #     result = response.results[0]
        #     if not result.alternatives:
        #         continue
        #     transcript = result.alternatives[0].transcript
        #     if result.is_final:
        #         self.transcript = transcript
        num_chars_printed = 0
        for response in responses:
            if not response.results:
                continue

            # The `results` list is consecutive. For streaming, we only care about
            # the first result being considered, since once it's `is_final`, it
            # moves on to considering the next utterance.
            result = response.results[0]
            if not result.alternatives:
                continue

            # Display the transcription of the top alternative.
            transcript = result.alternatives[0].transcript

            # Display interim results, but with a carriage return at the end of the
            # line, so subsequent lines will overwrite them.
            #
            # If the previous result was longer than this one, we need to print
            # some extra spaces to overwrite the previous result
            overwrite_chars = " " * (num_chars_printed - len(transcript))

            if not result.is_final:                
                sys.stdout.write(transcript + overwrite_chars + "\r")
                sys.stdout.flush()

                num_chars_printed = len(transcript)

            else:
                self.transcript = transcript
                print(transcript + overwrite_chars)

                # Exit recognition if any of the transcribed phrases could be
                # one of our keywords.
                if re.search(r"\b(exit|quit)\b", transcript, re.I):
                    print("Exiting..")
                    break

                num_chars_printed = 0

    def process(self):
        """
        Audio stream recognition and result parsing
        """
        #You can add speech contexts for better recognition
        cap_speech_context = types.SpeechContext(phrases=["Add your phrases here"])
        client = speech.SpeechClient()
        config = types.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=self.rate,
            language_code=self.language,
            speech_contexts=[cap_speech_context,],
            model='command_and_search'
        )
        streaming_config = speech.StreamingRecognitionConfig(
            config=config,
            interim_results=True,
            single_utterance=False)
        audio_generator = self.stream_generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = client.streaming_recognize(streaming_config, requests)
        try:
            self.response_loop(responses)
        except:
            self.start()

    def stream_generator(self):
        while not self.closed:
            chunk = self.buff.get()
            if chunk is None:
                return
            data = [chunk]
            while True:
                try:
                    chunk = self.buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break
            yield b''.join(data)

    def write(self, data):
        """
        Writes data to the buffer
        """
        self.buff.put(data)

transcoder = None

@sockets.route('/stream')
def start_streaming(ws):    
    app.logger.info("Connection accepted")
    while not ws.closed:
        message = ws.receive()
        if message is None:
            app.logger.info("No message received...")
            continue

        if isinstance(message, bytearray):
            transcoder.write(message)
            transcoder.closed = False
            if transcoder.transcript:
                print(transcoder.transcript)
                ws.send(transcoder.transcript)
                transcoder.transcript = None
            continue

        data = json.loads(message)

        if data['event'] == "connected":
            app.logger.info("Connected Message received: {}".format(message))
        if data['event'] == "start":
            app.logger.info("Start Message received: {}".format(message))
        if data['event'] == "config":
            transcoder = Transcoder(
                encoding=data["format"],
                rate=data["rate"],
                language=data["language"]
            )
            transcoder.start()
        if data['event'] == "closed":
            app.logger.info("Closed Message received: {}".format(message))
            break



print("Starting Server!")


if __name__ == "__main__":
    
    app.logger.setLevel(logging.DEBUG)
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(('', HTTP_SERVER_PORT), app, handler_class=WebSocketHandler)
    print("Server listening on: http://localhost:" + str(HTTP_SERVER_PORT))
    # main()
    server.serve_forever()

