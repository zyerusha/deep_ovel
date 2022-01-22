## <span style="color: rgb(175, 75, 75)">*!!! Welcome to DeepOVel - Deep Object Velocity in Video !!!*</span>

This tool was developed as part of my capstone project for the UC San Diego Extension Machine Learning Engineering Bootcamp.
The tool aims to find the velocity of objects within a video using Deep Learning algorithms.
The output of this code produces a Flask web server that enables a user to upload a video via the web browser, the video is processed and the output returned is a .zip file containg: 
1. A copy of the original uploaded video 
2. A video with bounding boxes as an output from the Yolo & DeepSort algorithms
3. A video with the estimated velocities of the detected objects
4. A .csv file containing all of the outputs of the tool

The main server page will look something like this:  
![image](https://user-images.githubusercontent.com/11064132/150650186-d12c9a9c-12ff-41b5-a4f3-efe21bac5887.png)

To use this properly, the user should enter the correct camera/video parameters that are used for the velocity calculations. 
![image](https://user-images.githubusercontent.com/11064132/150624693-580ee295-5bc6-483c-acdd-703d429b6030.png)

The project is hosted on dockerhub and can be run with a docker call:
```
docker run -dP deep_ovel
```
or
```
docker run -dp <selected_port>:8080 --name <container_name> deep_ovel
```


## References
### Code:
I would like to acknowledge the following resources used in this project. A lot of the core python code was taken from the following repositories:  </br>
[1] https://github.com/nwojke/deep_sort </br>
[2] https://github.com/hunglc007/tensorflow-yolov4-tflite </br>
[3] https://github.com/AlexeyAB/darknet  & https://github.com/pjreddie/darknet: yolov3 & yolov4 weights/model </br>
[4] https://www.pyimagesearch.com/2015/02/16/faster-non-maximum-suppression-python/ </br>
[5] https://github.com/theAIGuysCode/yolov4-deepsort </br>

### Papers:
[1] Speed Estimation On Moving Vehicle Based On Digital Image Processing </br>
Danang Wahyu Wicaksono and Budi Setiyono; 2017 </br>
 </br>
[2] Vehicle speed detection in video image sequences using CVS method  </br>
Arash Gholami Rad, Abbas Dehghani and Mohamed Rehan Karim  2010 </br>
 </br>
[3] You Only Look Once: Unified, Real-Time Object Detection </br>
Joseph Redmon, Santosh Divvala, Ross Girshic, Ali Farhadi; 2016 </br>
 </br>
[4] YOLOv3: An Incremental Improvement  </br>
Joseph Redmon and Ali Farhadi; 2018 </br>
 </br>
[5] YOLOv4: Optimal Speed and Accuracy of Object Detection </br>
Alexey Bochkovskiy, Chien-Yao Wang, Hong-Yuan Mark Liao; 2020 </br>
 </br>
[6] Simple Online and Realtime Tracking with as Deep Assciation Metric </br>
Nicolai Wojke, Alex Bewley, Dietrich Paulus; 2017 </br>
 </br>
[7] Simple Online and Realtime Tracking
Alex Bewley , Zongyuan Ge, Lionel Ott, Fabio Ramos, Ben Upcroft; 2017 </br>
 </br>
## Dataset used to evaluate the model:
[1] VIRAT</br>
https://viratdata.org/  </br>
Videos: https://data.kitware.com/#collection/56f56db28d777f753209ba9f/folder/56f581ce8d777f753209ca43</br>
Latest most up to date annotations are the DIVA Annotation. This is a public repository of the VIRAT video data annotations as annotated by the IARPA DIVA program. </br>
Annotations can be found here: https://gitlab.kitware.com/viratdata/viratannotations

Annotations are in the format per: </br>
https://gitlab.kitware.com/meva/meva-data-repo/-/blob/master/documents/KPF-specification-v4.pdf


[2] AU-AIR Dataset </br>
https://bozcani.github.io/auairdataset  </br>
AU-AIR : Multi-modal UAV Dataset for Low Altitude Traffic Surveillance (bozcani.github.io) </br>
Bozcan, Ilker, and Erdal Kayaan. "AU-AIR: A Multi-modal Unmanned Aerial Vehicle Dataset for Low Altitude Traffic Surveillance." </br>
IEEE International Conference on Robotics and Automation (ICRA), 2020, to appear.




