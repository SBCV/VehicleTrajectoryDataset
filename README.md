# VehicleTrajectoryDataset

Scripts of the dataset corresponding to the paper [3D Vehicle Trajectory Reconstruction in Monocular Video Data Using Environment Structure Constraints](http://openaccess.thecvf.com/content_ECCV_2018/html/Sebastian_Bullinger_3D_Vehicle_Trajectory_ECCV_2018_paper.html).

The actual dataset can be requested on [this](https://www.iosb.fraunhofer.de/en/competences/image-exploitation/object-recognition/sensor-networks/trajectory-reconstruction.html) Fraunhofer IOSB webpage.
Download the following files from the ftp server:
		ground_truth_data.tar.gz 
		rendering_data.tar.gz
	Extract these into the same folder <dataset> (i.e. merge the contents)

That means, <dataset> should show the following structure:
	
	<dataset>
		general_ground_truth_files
		path_car_1_obj
		path_car_2_obj
		path_car_3_obj
		path_car_4_obj
		path_car_5_obj
		path_car_6_obj
		path_car_7_obj

In order to create convenient ground truth files clone this repository with the following command to make sure the submodule is correctly initialized:
```
git clone --recurse-submodules https://github.com/SBCV/VehicleTrajectoryDataset.git
```

Run the following command:
```
python Post_Processing.py
```
to automatically create a local copy of the config files.

This will create two config files, i.e. 

	VehicleTrajectoryDataset/Utility/CloudCompare/CloudCompare.cfg
	VehicleTrajectoryDataset/Config/config.cfg

The script relies on [CloudCompare](https://www.danielgm.net/cc/) to transform Vehicle Meshes. At least **version 2.10** is required. Set the path in ```CloudCompare.cfg``` to your CloudCompare executable. 

In ```config.cfg``` adjust the path pointing to the downloaded dataset.

Run the following command (again) to post-process the dataset:
```
python Post_Processing.py
```

Calibration of the camera used for rendering:

	focal_length: 2100 [pixel]
	cx = 960 [pixel] and cy = 540 [pixel] 
	(No radial distortion)
	width = 1920 [pixel] and height = 1080 [pixel]
	stereo_baseline = 0.3 [meter]
