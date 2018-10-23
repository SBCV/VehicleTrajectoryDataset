import os
from shutil import copyfile
from Utility.Logging_Extension import logger
from Utility.File_Handler.Trajectory_File_Handler import TrajectoryFileHandler
from Utility.OS_Extension import mkdir_safely
from Utility.CloudCompare.CloudCompare import CloudCompare

def copy_ground(gt_general_idp, gt_specific_idp, lazy):

    ground_model_ply_ofp = os.path.join(
        gt_specific_idp, 'Ground.ply'
    )

    if not lazy or not os.path.isfile(ground_model_ply_ofp):
        ground_model_ply_ifp = os.path.join(
            gt_general_idp, 'Ground.ply'
        )
        copyfile(ground_model_ply_ifp, ground_model_ply_ofp)


def copy_vehicle_for_each_time_step(gt_general_idp, gt_specific_dp, lazy):

    vehicle_model_name = os.path.basename(
        os.path.dirname(gt_specific_dp))
    vehicle_model_ply_ifp = os.path.join(
        gt_general_idp, vehicle_model_name, 'CarBody.ply')

    trajectory_ifp = os.path.join(
        gt_specific_dp,
        'animation_transformations.txt')

    camera_object_trajectory = TrajectoryFileHandler.parse_camera_and_object_trajectory_file(
        trajectory_ifp)

    vehicle_model_odp = os.path.join(
        gt_specific_dp,
        'object_ground_truth_in_world_ground_truth_coordinates')
    mkdir_safely(vehicle_model_odp)

    for frame_name in camera_object_trajectory.get_frame_names_sorted():
        logger.vinfo('frame_name', frame_name)
        obj_matrix_world = camera_object_trajectory.get_object_matrix_world(frame_name)
        vehicle_model_ply_ofp = os.path.join(vehicle_model_odp, frame_name + '.ply')

        CloudCompare.apply_transformation(
            vehicle_model_ply_ifp,
            obj_matrix_world,
            vehicle_model_ply_ofp,
            save_point_clouds=False,
            save_meshes=True,
            lazy=True)



def post_process_ground_truth(gt_specific_dp,
                              gt_general_idp):

    logger.info('create_ground_truth: ...')
    logger.vinfo('gt_specific_idp', gt_specific_dp)
    logger.vinfo('gt_general_idp', gt_general_idp)

    copy_ground(
        gt_general_idp,
        gt_specific_dp,
        lazy=True)

    copy_vehicle_for_each_time_step(
        gt_general_idp,
        gt_specific_dp,
        lazy=True)

    logger.info('create_ground_truth: Done')
