![aidio v1](https://img.shields.io/badge/aidio-v1-brightgreen.svg)
![hackumass](https://img.shields.io/badge/hackumass-2022-brightgreen.svg)
![accuracy](https://img.shields.io/badge/accuracy-97-yellow.svg)

## What AIdio does:

Uses Machine Learning to (1) convert American Sign Language to text and (2) convert real time live-stream speech to text. Circumvents racial and ethnic bias in training set due to original, self-made algorithm. Implemented with Python, HTML, CSS, JavaScript, and various other libraries.


### Inspiration

American Sign Language users can use our ASL-to-text platform as a means of learning, getting instant feedback on signed word arrangements, and as a means of expression to communicate with non-ASL users. Our video call-based speech-to-text converter also hosts transcribing capabilities not yet offered on popular platforms like WhatsApp, Line, and Discord. Heightened by COVID-19, those who are hard of hearing might have difficulty lip-reading or be unable to reproduce real life conversations over online platforms due to a host of reasons.

We want to improve current transcription models and make web calling more accessible.

## Table of Contents:
- [Features](#features)
- [Technologies](#technologies)
- [Accomplishments](#accomplishment)
- [Deploying Locally](#deploying-locally)
- [Contributors](#contributors)
## Features: 

We use a total of three Machine Learning models: (1) identify hand joints for training data, (2) recognize American Sign Language words, and (3) process speech to text.

### ASL-to-Text

Early on in the project, we had trouble finding ways to identify ASL hand signs efficiently in less than HackUMass' designated 36 hours. Passing in pixelated videos and pictures as parameters to Tensorflow takes several hours to days to render and process because colors and exact coordinates are passed directly into the CNN model.

Our solution is to map hand joints, normalize the ratio of each joint to a certain point at the bottom of the hand between the range [0,-1], and pass in a CSV file of matrices (containing only floats). This way, we are able to train our model at a much faster rate and load the data within the bounds of one hour compared to the many hours a CNN would take. The entire dataset is produced by our team. Our lighting in a moderately lit classroom has almost no impact on our results. Likewise, due to the lack of parametrized RGB values, there is no ethnic or racial bias in our model.

### Speech-to-Text

We are using a Natural Language Processor (NLP) with Tensorflow to process English. Our main difficulty was configuring different devices to have cross-chatting capabilities. We used Sockets and Flask to handle the back-end, OpenCV for video streaming, and Python script.


## Challenges:

Learning how to create and use a large data (in excess of over 200 images per word) to train the model. Our solution is described under the "how we built it" section.

Creating an online video-chatting system similar to Zoom on our website. We have to host our own platform from scratch.

Configuring versions of Python to be compatible with different libraries. For an example, we had issues installing pyaudio (and similarly portaudio for building the wheels of this module) on three of the four computers, Mediapipe, and Tensorflow. These libraries often work with very specific versions like Python 3.10.8 rather than 3.11 which is the newest version. 

## Technologies:
- Tensorflow
- GoogleCloud API
- openCV/ cv2
- Python/ Flask/ Blueprints
- Websockets
- Numpy
- JavaScript/HTML/CSS

## Accomplishments:

We trained, processed, and deployed state-of-the-art, custom-made Machine Learning models and achieved a very high accuracy rate of above 97% for our ASL-to-text converter. Similarly, for the second part of our project, we successfully launched a web call client despite facing difficulties from security proxies, video lag disparities, and other related issues.

Every member of our team contributed wholeheartedly so we could complete our project in time. We slept an average of less than three hours each the during the entire duration of the weekend. To train three different models, we had to exercise a great deal of patience with bugs.

## Future Directions

With the exponentially low storage and time requirements compared to most industrial training methods, we look forward to incorporating a more diverse dictionary of words and signs. We also hope to develop maintain an open source training platform, while researching and enabling the visualization of moving signs. We are also looking at other potential implimations of our model for low-scale rollout. Our model surpasses most other CNN models in terms of speed and ease of uploading new files, and we would love to help make the world more accessible.


## Deploying locally:

Clone the repository at: 
```
gh repo clone coolkite/AIdio
```
You want to clone the Website branch, not the main branch

Install tensorflow, pyaudio, flask_sockets, and opencv-python using: 
```
python3 -m pip install <requirement-name>
```

Run main.py file

## Contributors:
<table>
  <tr>
    <td align="center"><a href="https://github.com/coolkite"><img src="" width="100px;" alt=""/><br /><sub><b>Divyansh Shivashok </br> dshivashok@umass.edu </b></sub></a></td>
    <td align="center"><a href="https://github.com/zaranip"><img src="" width="100px;" alt=""/><br /><sub><b>Zara Nip </br> znip@umass.edu </b></sub></a></td>
    <td align="center"><a href="https://github.com/Tapugy"><img src="" width="100px;" alt=""/><br /><sub><b>Jacob Cohen </br> jicohen@umass.edu</b></sub></a></td>
    <td align="center"><a href="https://github.com/dmtrung14"><img src="" width="100px;" alt=""/><br /><sub><b>Trung Dang </br> tmdang@umass.edu </b></sub></a></td>
  </tr>
  <tr>
    <td align="center"><sub><b>Team Leader</br>Head Machine Learning Engineer</b></sub></a></td>
    <td align="center"><sub><b>Lead Front-end Engineer</br>Full-Stack Assistant</b></sub></a></td>
    <td align="center"><sub><b>Lead Back-end Engineer</b></sub></a></td>
    <td align="center"><sub><b>Lead Data Engineer and Deployment</br>Full Stack Assistant</b></sub></a></td>
  </tr>
</table>
