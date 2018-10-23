from PIL import ImageFile
import os
from Utility.Types.Point import Point
from Utility.Logging_Extension import logger
from Utility.File_Handler.EXR_File_Handler import EXRFileHandler
from Utility.File_Handler.NVM_File_Handler import NVMFileHandler
from Utility.File_Handler.Trajectory_File_Handler import TrajectoryFileHandler
from Collect_Image_Paths import get_image_paths_in_folder


def post_process_depth_output(model_idp,
                              animation_transformations_file_suffix,
                              input_depth_image_folder_name,
                              output_nvm_folder_name,
                              lazy=True):

    logger.info('post_process_depth_output: ...')

    # Input path
    input_depth_image_folder_path = os.path.join(model_idp, input_depth_image_folder_name)
    animation_transformations_file = os.path.join(
        model_idp, animation_transformations_file_suffix)

    if os.path.isdir(input_depth_image_folder_path):

        # Output path
        nvm_folder_path = os.path.join(model_idp, output_nvm_folder_name)
        if not os.path.isdir(nvm_folder_path):
            os.mkdir(nvm_folder_path)
        logger.vinfo('nvm_folder_path', nvm_folder_path)

        input_depth_list = get_image_paths_in_folder(
            input_depth_image_folder_path, ext='.exr')

        # Required to avoid "IOError: broken data stream when reading image file" error
        ImageFile.LOAD_TRUNCATED_IMAGES = True

        camera_object_trajectory = TrajectoryFileHandler.parse_camera_and_object_trajectory_file(
            animation_transformations_file)

        logger.vinfo('camera_object_trajectory', camera_object_trajectory)

        for input_depth_exr_path in input_depth_list:
            frame_exr_name = os.path.basename(input_depth_exr_path)
            frame_exr_name_stem = os.path.splitext(os.path.basename(frame_exr_name))[0]
            frame_jpg_name = frame_exr_name_stem + '.jpg'
            output_nvm_path = os.path.join(nvm_folder_path, frame_exr_name_stem) + '.nvm'

            logger.vinfo('output_nvm_path', output_nvm_path)

            nvm_file_missing = not os.path.isfile(output_nvm_path)

            if nvm_file_missing or not lazy:

                exr_data_as_np = EXRFileHandler.parse_depth_exr_file(input_depth_exr_path)
                height, width = exr_data_as_np.shape

                cam = camera_object_trajectory.get_camera(frame_jpg_name)
                cam.file_name = frame_jpg_name
                cam.height = height
                cam.width = width
                logger.vinfo('width', width)
                logger.vinfo('height', height)
                cameras = [cam]

                coords_world_coord = cam.convert_depth_buffer_to_world_coords(
                    exr_data_as_np,
                    invert_y=True)

                points = []
                for coord in coords_world_coord:
                    points.append(Point(coord=coord))

                NVMFileHandler.write_nvm_file(output_nvm_path, cameras, points)

    else:
        logger.info('EXR FOLDER MISSING, SKIPPING ...')

    logger.info('post_process_depth_output: Done')