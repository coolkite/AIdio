What AIdio does:

Uses Machine Learning to (1) convert American Sign Language to text and (2) convert real time live-stream speech to text. Circumvents racial and ethnic bias in training set due to original, self-made algorithm. Implemented with Python, HTML, CSS, JavaScript, and various other libraries.

Why the project is useful and inspiration:

American Sign Language users can use our ASL-to-text platform as a means of learning, getting instant feedback on signed word arrangements, and as a means of expression to communicate with non-ASL users. Our video call-based speech-to-text converter also hosts transcribing capabilities not yet offered on popular platforms like WhatsApp, Line, and Discord. Heightened by COVID-19, those who are hard of hearing might have difficulty lip-reading or be unable to reproduce real life conversations over online platforms due to a host of reasons. We hope our web app can circumvent that.


How we built it:

We use a total of three Machine Learning models: (1) identify hand joints for training data, (2) recognize American Sign Language words, and (3) process speech to text.

ASL-to-Text

Early on in the project, we had trouble finding ways to identify ASL hand signs efficiently in less than HackUMass' designated 36 hours. Passing in pixelated videos and pictures as parameters to Tensorflow takes several hours to days to render and process because colors and exact coordinates are passed directly into the CNN model.

Our solution is to map hand joints, normalize the ratio of each joint to a certain point at the bottom of the hand between the range [0,-1], and pass in a CSV file of matrices (containing only floats). This way, we are able to train our model at a much faster rate and load the data within the bounds of one hour compared to the many hours a CNN would take. The entire dataset is produced by our team. Our lighting in a moderately lit classroom has almost no impact on our results. Likewise, due to the lack of parametrized RGB values, there is no ethnic or racial bias in our model.

Speech-to-Text

We are using a Natural Language Processor (NLP) with Tensorflow to process English. Our main difficulty was configuring different devices to have cross-chatting capabilities. We used Sockets and Flask to handle the back-end, OpenCV for video streaming, and Python script.


Challenges we ran into:

Learning how to create and use a large data (in excess of over 200 images per word) to train the model. Our solution is described under the "how we built it" section.

Creating an online video-chatting system similar to Zoom on our website. We have to host our own platform from scratch.

Configuring versions of Python to be compatible with different libraries. For an example, we had issues installing pyaudio (and similarly portaudio for building the wheels of this module) on three of the four computers, Mediapipe, and Tensorflow. These libraries often work with very specific versions like Python 3.10.8 rather than 3.11 which is the newest version. 


Accomplishments you are proud of:

We trained, processed, and deployed state-of-the-art, custom-made Machine Learning models and achieved a very high accuracy rate of above 97% for our ASL-to-text converter. Similarly, for the second part of our project, we successfully launched a web call client despite facing difficulties from security proxies, video lag disparities, and other related issues.

Every member of our team contributed wholeheartedly so we could complete our project in time. We slept an average of less than three hours each the during the entire duration of the weekend. To train three different models, we had to exercise a great deal of patience with bugs.


What you learned:

All of us learned about deploying Tensorflow and other related Machine Learning libraries. Additionally, we had to actively incoporate information about many internet protocols like File Transfer Protocol (FTP), Transfer Control Protocol (TCP), and limitations of Eduroam in our code to ensure that our video chat platform would launch correctly.


What's next for our hack:

Expanding our library of ASL words! With our automated data training methodology (script found in this Github), we can continually push new words into our model in 10 minutes or less. We are also looking at other potential implimations of our model for low-scale rollout. Our model surpasses most other CNN models in terms of speed and ease of uploading new files, and we would love to help make the world more accessible.


How users can get started with the project:

Head to our python-implemented models on our website. 


Where users can get help with your project: 

dshivashok@umass.edu, tmdang@umass.edu, znip@umass.edu, jicohen@umass.edu


Who maintains and contributes to the project:

Divyansh, Zara, Jacob, and Trung for 2022 HackUMass  
dshivashok@umass.edu, znip@umass.edu, jicohen@umass.edu, tmdang@umass.edu
