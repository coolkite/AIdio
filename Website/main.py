from flask import Flask, render_template, Response, url_for
#from camera import VideoCamera
# from stt_script import *

import argparse
import copy
import itertools
import time

import cv2
from cv2 import rectangle
import mediapipe as mp
import numpy as np
import tensorflow as tf


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("Demo.html")


#def gen(camera):

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--width", help='cap width', type=int, default=960)
    parser.add_argument("--height", help='cap height', type=int, default=540)

    parser.add_argument('--use_static_image_mode', action='store_true')
    parser.add_argument("--min_detection_confidence",
                        help='min_detection_confidence',
                        type=float,
                        default=0.7)
    parser.add_argument("--min_tracking_confidence",
                        help='min_tracking_confidence',
                        type=int,
                        default=0.5)

    args = parser.parse_args()

    return args


def main():
    args = get_args()

    cap_device = args.device
    cap_width = args.width
    cap_height = args.height

    use_static_image_mode = args.use_static_image_mode
    min_detection_confidence = args.min_detection_confidence
    min_tracking_confidence = args.min_tracking_confidence

    vid = cv2.VideoCapture(cap_device)
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, cap_width)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_height)

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands

    hands = mp_hands.Hands(
            static_image_mode=use_static_image_mode,
            max_num_hands=1,
            model_complexity=0,
            min_detection_confidence = min_detection_confidence,
            min_tracking_confidence= min_tracking_confidence
            )

    model = tf.keras.models.load_model('finalV4.h5')
    mapping = {
                0:"0",
                1:"1",
                2:"2",
                3:"3",
                4:"4",
                5:"5",
                6:"F",
                7:"7",
                8:"8",
                9:"6",
                10:"A",
                11:"B",
                12:"C",
                13:"D",
                14:"E",
                15:"9",
                16:"G",
                17:"H",
                18:"I",
                19:"J",
                20:"K",
                21:"L",
                22:"M",
                23:"N",
                24:"O",
                25:"P",
                26:"Q",
                27:"R",
                28:"S",
                29:"T",
                30:"U",
                31:"V",
                32:"W",
                33:"X",
                34:"Y",
                35:"Z",
                36:"SPACE"
            }
    

#do some stuff
    frameCount = 0
    spaceCount = 0
    sentence = ""
    
    while True:
        ret, frame = vid.read()
        if ret == False:
            break
        
        frame = cv2.flip(frame, 1)
        frameCopy = copy.deepcopy(frame)

        frame.flags.writeable = False
        frame = cv2.cvtColor(frameCopy, cv2.COLOR_BGR2RGB)
        results = hands.process(frame)

        frame.flags.writeable = True

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                frameCount += 1
                handCoordinates = []
                frame_W = frameCopy.shape[1]
                frame_H = frameCopy.shape[0]

                for landmarks in hand_landmarks.landmark:
                    landmark_x = min(int(landmarks.x * frame_W), frame_W - 1)
                    landmark_y = min(int(landmarks.y * frame_H), frame_H - 1)
                    handCoordinates.append([landmark_x, landmark_y])

                #print(handCoordinates)
                flattened = copy.deepcopy(handCoordinates)
                bX, bY = 0, 0
                for i in range(len(flattened)):
                    if i==0:
                        bX = flattened[0][0]
                        bY = flattened[0][1]
                    
                    flattened[i][0] = flattened[i][0] - bX
                    flattened[i][1] = flattened[i][1] - bY
                
                #print(flattened)
                flattened = list(itertools.chain.from_iterable(flattened))
                argMax = max(list(map(abs, flattened)))
                
                for i in range(len(flattened)):
                    flattened[i] /= argMax


                prediction = model.predict(np.array([flattened]))
                squeezed = np.squeeze(prediction)
                result = mapping[np.argmax(squeezed)]
                print(frameCount)
                if frameCount == 15:    
                    if result == "SPACE":
                        sentence += " "
                        spaceCount += 1

                    elif spaceCount < 3:
                            sentence += result

                    else:
                        spaceCount = 0
                        sentence = ""
                    frameCount = 0


                print(sentence)
                mp_drawing.draw_landmarks(
                    frameCopy,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )
                    
                    
            cv2.putText(frameCopy, 
                        result, 
                        (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        1, 
                        (0, 255, 255), 
                        2, 
                        cv2.LINE_4)

            rectangle(frameCopy, (380, 570), (425+len(sentence)*20, 615), (0, 0, 0), -1)
            cv2.putText(img=frameCopy, text=sentence, org=(400, 600), fontFace=cv2.FONT_HERSHEY_COMPLEX , fontScale=1, color=[0, 0, 0], lineType=cv2.LINE_AA, thickness=4)
            cv2.putText(img=frameCopy, text=sentence, org=(400, 600), fontFace=cv2.FONT_HERSHEY_COMPLEX , fontScale=1, color=[255, 255, 255], lineType=cv2.LINE_AA, thickness=2)
        cv2.imshow('hand detection', frameCopy)        
        # if cv2.waitKey(5) & 0xFF == ord('q'):
        #     break
        
#     vid.release()
#     cv2.destroyAllWindows()
        ret, jpeg = cv2.imencode('.jpg', frameCopy)
        frameCopy = jpeg.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frameCopy + b'\r\n\r\n')
        
    # while True:
    #     frame = camera.get_frame()
        


@app.route('/video_feed')
def video_feed():
    return Response(main(), mimetype='multipart/x-mixed-replace; boundary=frame')
# def reprint(output):
#     while True:
#         frame = output.main()
#         yield ( frame )

@app.route('/Algorithm.html')
def algorithm():
    return render_template('/Algorithm.html')

@app.route('/blog.html')
def blog():
    return render_template('/blog.html')
@app.route('/Diversity.html')
def diversity():
    return render_template('/Diversity.html')
@app.route('/Home.html')
def home():
    return render_template('/Home.html')
@app.route('/Our-Team.html')
def ourteam():
    return render_template('/Our-Team.html')
@app.route('/Demo.html')
def demo():
    return render_template('/Demo.html')
if __name__ == "__main__":
    app.run(host = "0.0.0.0", port='5000', debug=True)