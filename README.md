# <span style="color: rgb(175, 75, 75)">*!!! Welcome to DeepOVel - Deep Object Velocity in Video !!!*</span>
## Introduction
As a means of improving smart traffic monitoring within an urban setting, there is a need to be able to estimate velocities of moving objects (cars, humans). Doing so will help in detecting and mitigating traffic congestion. By leveraging existing camera infrastructure on the roadways, video feed can estimate the velocity of the object thus alerting other systems and helping alleviate the traffic bottlenecks.  <br>
My  objective in this project was to be able to estimate the velocity of moving objects within a video using Deep Learning algorithms. </br>  
This tool was developed as part of my capstone project for the UC San Diego Extension Machine Learning Engineering Bootcamp.</br></br>
### Object detection and classification
The tool leverages the [YOLO - You Only Look Once](https://arxiv.org/abs/1506.02640) algorithm (Redmon et al., 2015) for image detection and classification. YOLO is considered to be extremely fast versus other image detection and classification methods, such as [Histogram of Oriented Gradients (HOG)](https://ieeexplore.ieee.org/abstract/document/1467360) (N. Dalal; B. Triggs, 2005); [Single Shot Detector (SSD)](https://arxiv.org/abs/1512.02325); or Region-based Convolutional Neural Networks (R-CNN) and it’s variants: Fast R-CNN, and [Faster R-CNNs](https://arxiv.org/abs/1506.01497) (Ren et al., 2015), [Mask R-CNN](https://www.analyticsvidhya.com/blog/2019/07/computer-vision-implementing-mask-r-cnn-image-segmentation/) for Image Segmentation; </br> 

Speed comparison between different detection methods ([source](https://cv-tricks.com/object-detection/faster-r-cnn-yolo-ssd/)): </br>
![image](https://user-images.githubusercontent.com/11064132/155455879-7434d454-0c56-4b3f-8d30-5d96375548ce.png) </br>


In general, YOLO works on the concept of dividing each image into a grid of S x S and each grid predicts N bounding boxes and confidence. </br> 
The confidence reflects the accuracy of the bounding box and whether the bounding box actually contains an object. YOLO also predicts the classification score of each class it was trained on. The probability of an object of a specific class being in a bounding box can then be calculated.  </br>
A total SxSxN boxes are predicted and since most of these boxes have low confidence scores, a threshold is applied on the confidence and boxes with low confidence are removed. 
As a note, one drawback of YOLO is that it only predicts 1 type of class in one grid therefore it struggles  detecting small objects. </br></br>

YOLO object detection pipeline ([source](https://arxiv.org/abs/1506.02640)): </br>
![image](https://user-images.githubusercontent.com/11064132/155456205-5cbb1cde-67e5-47bb-9ec2-012a55230ee0.png) </br>
</br>

The YOLO algorithm does not apply [non-maxima suppression](https://pyimagesearch.com/2014/11/17/non-maximum-suppression-object-detection-python/?_ga=2.266530702.1041006104.1640999966-2035547223.1637780419), therefore it needs to be explicitly applied to suppress significantly overlapping bounding boxes, keeping only the most confident ones.  </br></br>

### Object Tracking
In order to continuously track objects along multiple frames, each object must be uniquely identified between consecutive frames. To accomplish this, the [DeepSORT](https://arxiv.org/abs/1703.07402) algorithm was chosen since it is suited for real time applications. DeepSORT is based on the [Simple Online and Realtime Tracking (SORT)](https://arxiv.org/abs/1602.00763) algorithm.  Much of the computational complexity is done during the offline pre-training stage where a deep association metric on a large-scale re-identification dataset is learned. When the application is running online, it leverages nearest neighbor queries in visual appearance space and the algorithm performs measurement-to-track associations. With DeepSORT, objects can be tracked through longer periods of occlusions effectively reducing the number of identity switches. </br></br>

### Velocity Estimation
The geometric calculation for velocity estimation is performed by using properties of the camera/image and  computation made for the distance of an object based on the camera field of view and height (see [Speed Estimation On Moving Vehicle Based On Digital Image Processing](https://www.researchgate.net/publication/317312246_Speed_Estimation_On_Moving_Vehicle_Based_On_Digital_Image_Processing)).</br></br>

### Project Output</br>
The output of this code produces a Flask web server that enables a user to upload a video via the web browser.  The video is processed and returned in the form of a .zip file containing: </br>
- A copy of the original uploaded video  </br>
- video with bounding boxes as an output from the Yolo & DeepSort algorithms </br>
- video with the estimated velocities of the detected objects </br>
- .csv file containing all of the outputs of the tool </br>


![image](https://user-images.githubusercontent.com/11064132/150652498-d252d0bf-fc43-404e-99c3-e2c97b2b347a.png)


</br>
<img src="https://user-images.githubusercontent.com/11064132/150653665-94e447be-5d24-429f-b9df-888453adc920.png" alt="drawing" width="700"/>
<img src="https://user-images.githubusercontent.com/11064132/150653860-2ec97e7d-b016-4669-a368-194113090ed6.png" alt="drawing" width="700"/>

___


### The main server page will look something like this:  
![image](https://user-images.githubusercontent.com/11064132/150650186-d12c9a9c-12ff-41b5-a4f3-efe21bac5887.png)


To properly use this tool, the user should enter the correct camera/video parameters that are used for the velocity calculations. 


The project is hosted on [dockerhub](https://hub.docker.com/r/zyerusha/deep_ovel). </br>
Pull by calling: ```docker pull zyerusha/deep_ovel``` </br>
To run use: </br>
```
docker run -dP zyerusha/deep_ovel
```
or
```
docker run -dp <selected_port>:8080 --name <container_name> zyerusha/deep_ovel
```
Then open a web browser to: </br>
"localhost:<selected_port>" 
___


## High Level overview of source files
| Code | Description |
| :----- | :----- |
|./main_app.py | Is the main entry point. Starts the Flask server |
|./app_config.py | Configures the Flask server|
|./deep_ovel.py | The DeepOVel class manages the application and the "glue" between the Yolo-DeepSORT bounding boxes calculations and the velocity calculation. It is the main interaction with Flask server via the Run() method |
|./deepsort_yolo.py | DeepsortYolo class manages the processing of the video, initializes and runs Yolo and DeepSORT.  The output is a processed video and dataframe with the calculations |
|./templates/client/ | Contains HTMLs for the website used by Flask |
|./static/media/  | Contains media used by the server |
|./tf_yolov4/   | Main engine that runs the YOLO algorithm using tensorflow. Converts YOLOv4 to .pb, .tflite and trt format for tensorflow (https://github.com/hunglc007/tensorflow-yolov4-tflite). Minor modifications were made |
|./app_utils/  | Contains utilities to perform different operations |
|./deepsort/  |  Main engine that runs the DeepSORT algorithm (https://github.com/nwojke/deep_sort) with minor modifications. |


## Further work:
- [ ] Train the YOLO weights and optimize on better identifying vehicles and people from top view. One major flaw with the current image detection and tracking is that identification of objects (cars and humans) is not very successful from above with the current weights used.
- [ ] Improve and optimize training of the YOLO detection and classification to more relevant objects (e.g. vehicles, humans, watercraft, aircraft).
- [ ] The velocity calculations are very susceptible to jitter in the image tracking. There have been efforts to filter this but there is room for improvement.
- [ ] With the current implementation, to get decent velocity estimations, the camera parameters must be inputted. Ideally, the velocity would be calculated using the size of the object that was identified based on the classification produced by YOLO. 
 
 
 ___


## Acknowledgements
Special thanks to [Zuraiz Uddin](https://www.linkedin.com/in/zuraiz-uddin-99600296) for his mentorship and guidance while working on this project.

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
[6] Simple Online and Realtime Tracking with as Deep Association Metric </br>
Nicolai Wojke, Alex Bewley, Dietrich Paulus; 2017 </br>
```
@inproceedings{Wojke2017simple,
  title={Simple Online and Realtime Tracking with a Deep Association Metric},
  author={Wojke, Nicolai and Bewley, Alex and Paulus, Dietrich},
  booktitle={2017 IEEE International Conference on Image Processing (ICIP)},
  year={2017},
  pages={3645--3649},
  organization={IEEE},
  doi={10.1109/ICIP.2017.8296962}
}
@inproceedings{Wojke2018deep,
  title={Deep Cosine Metric Learning for Person Re-identification},
  author={Wojke, Nicolai and Bewley, Alex},
  booktitle={2018 IEEE Winter Conference on Applications of Computer Vision (WACV)},
  year={2018},
  pages={748--756},
  organization={IEEE},
  doi={10.1109/WACV.2018.00087}
}
```
 </br>
[7] Simple Online and Realtime Tracking
Alex Bewley , Zongyuan Ge, Lionel Ott, Fabio Ramos, Ben Upcroft; 2017 </br>
 </br>
 
## Dataset used to evaluate the model:  
[1] VIRAT https://viratdata.org/  </br>
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

</br>

## Thanks for your interest!</br>
I hope you found this repo and tool helpful.  If you have any questions or comments, feel free to reach out on [LinkedIn](https://www.linkedin.com/in/zafrir-zeph-y-94568210)



