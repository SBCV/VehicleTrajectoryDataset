# VehicleTrajectoryDataset

Scripts of the dataset corresponding to the paper [3D Vehicle Trajectory Reconstruction in Monocular Video Data Using Environment Structure Constraints](http://openaccess.thecvf.com/content_ECCV_2018/html/Sebastian_Bullinger_3D_Vehicle_Trajectory_ECCV_2018_paper.html).

The actual dataset can be requested on [this](http://s.fhg.de/trajectory) Fraunhofer IOSB webpage.

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
  ```VehicleTrajectoryDataset/Utility/CloudCompare/CloudCompare.cfg```
  ```VehicleTrajectoryDataset/Config/config.cfg```

The script relies on CloudCompare [CloudCompare](https://www.danielgm.net/cc/) to transform Vehicle Meshes. At least **version 2.10** is required. Set the path in ```CloudCompare.cfg``` to your CloudCompare executable. 

In ```config.cfg``` adjust the path pointing to the downloaded dataset.

Run the following command (again) to post-process the dataset:
```
python Post_Processing.py
```
