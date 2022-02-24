## <span style="color: rgb(175, 75, 75)">*!!! Welcome to DeepOVel - Deep Object Velocity in Video !!!*</span>
### Introduction
As a means of improving smart traffic monitoring within an urban setting, there is a need to be able to estimate velocities of moving objects (cars, humans). Doing so will help in detecting and mitigating traffic congestion. By leveraging existing camera infrastructure on the roadways, video feed can estimate the velocity of the object thus alerting other systems and helping alleviate the traffic bottlenecks.  <br>
My  objective in this project was to be able to estimate the velocity of moving objects within a video using Deep Learning algorithms. <br>  
This tool was developed as part of my capstone project for the UC San Diego Extension Machine Learning Engineering Bootcamp.
</br>
The output of this code produces a Flask web server that enables a user to upload a video via the web browser.  The video is processed and returned in the form of a .zip file containing: 
- [x] A copy of the original uploaded video 
- [x] A video with bounding boxes as an output from the Yolo & DeepSort algorithms
- [x] A video with the estimated velocities of the detected objects
- [x] A .csv file containing all of the outputs of the tool


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



