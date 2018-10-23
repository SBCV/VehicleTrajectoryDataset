# VehicleTrajectoryDataset

Scripts of the dataset corresponding to the paper [3D Vehicle Trajectory Reconstruction in Monocular Video Data Using Environment Structure Constraints](http://openaccess.thecvf.com/content_ECCV_2018/html/Sebastian_Bullinger_3D_Vehicle_Trajectory_ECCV_2018_paper.html).

The actual dataset can be requested on [this](http://s.fhg.de/trajectory) Fraunhofer IOSB webpage.


Clone the repository with the following command to make sure the submodule is correctly initialized:

```
git clone --recurse-submodules https://github.com/SBCV/VehicleTrajectoryDataset.git
```

Run the following command to post-process the dataset:
```
python Post_Processing.py
```
The first excecution will create a file ``` config.cfg ```.
Adjust the values in this config file as required and run the above command again.

