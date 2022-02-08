There are lots of devices that need special effort to communicate with computer, making it hard to monitor or record the data easily.

This program is used to extract data from all kinds of devices with 7 segments digit readings, by using a camera point at the device.

1,Requirement
Python 3+
Python libraries: datetime,json,matplotlib,numpy,pillow,statistics,imutils, openvc-python,scipy,
google-cloud-storage

2,instruction on using
The program consist of four .py files: 'analyze_GUI 2.py', 'image_acquare_extract.py', 'upload.py', 'web.py'. 

The script 'image_acquare_extract.py' can capture video from camera and extract the digits from it, save the data in form of readings and time, then save as one file in the local, one file in the cloud google Drive.The file contains all the data start from this run and updated very fast with the feeding video. 

The script 'analyze_GUI 2.py' can download the data from cloud google Drive and analyze it, showing a plot of the data versus time and some statistics. You can set the upper and lower limit and provide your email address, if the data is over the limit you set, you will receive a warning email with a picture of the plot. 

In real situation, 'image_acquare_extract.py' should be ran on a data collecting computer with camera aimed to the device.'analyze_GUI 2.py' should be ran on another computer at anytime you want to show you the plot,statistics and warning email function.

The script 'upload.py' and 'web.py' are modules consist of functions which are used in the two main script. You can ignore these two.

There are also two extra files named 'analyze_GUI with test data.py' and 'image_acquare_extract on one iamge(for test).py'. These two are for test purpose only. When you don't have a device and camera with you to set up a complete system, you could first run 'image_acquare_extract on one iamge(for test).py' to collect the data from one single image, and  run 'analyze_GUI with test data.py' can test the statistics and warning email function from one set of test data measured by me.

3,features
The program take advantage of 7 segments readings and extract the features from image to get the digits, which cost less time and effort than OCR.

The digits recognition process is set to have a big tolerance with little constrain on the position or size of the digits. It can recognize both bright digits and dark digits and store the data in cloud for remote access. 

The analysis and GUI part can download and analyze the data from Google Drive and allow the user to set and change upper or lower limit, warning email receiver at any time. 
If the reading is over the limit, one warning email will be sent to the receiver with a picture of the data attached. But if the set limit is not changed, the warining email will be deactivated to avoid cramming the inbox.If the limit is changed, the warning email will be activated again. A copy of the data will also be saved locally for convenience of furthur reference.

4,Improvements
The digits recognition code is not robust enough, especially for dark digits, the user still need to adjust the position and angle of the camera and avoid strong enviromental light polution. And also sometimes the recognition will miss one or add one more digits, this behavior is cleaned at the begining of 'analyze_GUI 2.py'. But it is still a potential hazard to robustness.


