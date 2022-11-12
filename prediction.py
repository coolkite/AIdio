import argparse
import copy
import itertools

import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf


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
            max_num_hands=2,
            model_complexity=0,
            min_detection_confidence = min_detection_confidence,
            min_tracking_confidence= min_tracking_confidence
            )

    model = tf.keras.models.load_model('9422v1.h5')

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
                result = np.argmax(squeezed)
                
                mp_drawing.draw_landmarks(
                    frameCopy,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                    )
                    
                cv2.putText(frameCopy, 
                            str(result), 
                            (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            1, 
                            (0, 255, 255), 
                            2, 
                            cv2.LINE_4)
        cv2.imshow('hand detection', frameCopy)
        
        
        
        
        
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
        
    vid.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
