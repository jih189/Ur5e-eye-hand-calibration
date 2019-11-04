1. install visp with
	sudo apt-get install libvisp-dev libvisp-doc visp-images-data

2. go to cali/calibration with cd cali/calibration and create build directory and build with
	cd ~/cali/calibration
	mkdir build
	cmake ..
	make

3. go back to ~/cali

4. get the pose of the hand and image from camera with
	python get_pose_and_image.py [index of image]
   where index of image should start from 1.
   You can type 'q' for exitting the program, or use 't' to recore the pose and image. If you think the image is not captured well, you can type any key to retake image.
   for example if you need 3 images for calibration, you should type:
	python get_pose_and_image.py 1
	python get_pose_and_image.py 2
	python get_pose_and_image.py 3
   then, you will have
	image-[imageIndex].jpg and pose_fPe_[imageIndex].yaml

3. convert angle from quaternion to theta U form

   everytime you capture a image and pose, it will output four number for angle. Then you need to convert it from quaternion to theta U form.
   copy those four number from
	
	found board
	please copy following number:

	0.0229401117969   0.119348563488   0.560558129947   -0.819148493629

   and pass them to convertAngle by
	./convertAngle 0.0229401117969   0.119348563488   0.560558129947   -0.819148493629
   then you will got

	x:0.0229401117969
	y:0.119348563488
	z:0.560558129947
	w:-0.819148493629
	result:
	-0.04886300951
	-0.2542154071
	-1.194002776
	copy following data and append them to yaml file
	  - [-0.04886300951]
	  - [-0.2542154071]
	  - [-1.194002776]

   then you need to copy and append last three lines to pose_fPe_[imageIndex].yaml.

4. need to repeat step 2 and 3 nine times, and run
	python getCameraIntri.py
   it will output camera parameter

5. put the camera parameter in to camera.xml and copy it to "build"

6. modify the camera parameter in "get-chessboard-pose.cpp" where
	 cam.initPersProjWithoutDistortion(2741.8, 2736.8, 1321.5, 946);

   and run make in build again.

6. copy all image-[imageIndex].jpg and pose_fPe_[imageIndex].yaml to build, and run
	./get-chessboard-pose --input image-%d.jpg

7. run
	./hand-eye-calibration --ndata [number of image]

then you got the transformation from hand pose to camera pose. you can use add_wrist_camera_frame.py to verify the pose.


