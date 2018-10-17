
import os

from Segmentation_Output_Post_Processing import post_process_segmentation_output
from Depth_Output_Post_Processing import post_process_depth_output

from Utility.Logging_Extension import logger
from Utility.Config import Config

def perform_post_processing(path_to_environment_output,
                            create_depth_files=False,
                            lazy=True):

    logger.info('perform_post_processing: ...')
    logger.info('path_to_environment_output: ' + path_to_environment_output)
    target_suffix = '_frames_jpg'

    video_name = 'virtual.avi'
    video_frame_rate = 12.5
    rendered_image_folder_name = \
        os.path.splitext(video_name)[0] + \
        '_fr_' + str(video_frame_rate) + '_frames_jpg'

    object_mask_image_folder_name = \
        os.path.splitext(video_name)[0] + \
        '_fr_' + str(video_frame_rate) + '_object_mask_jpg'
    object_image_output_folder_name = \
        os.path.splitext(video_name)[0] + '_fr_' + \
        str(video_frame_rate) + '_object_jpg'
    object_h5_output_folder_name = \
        os.path.splitext(video_name)[0] + '_fr_' + \
        str(video_frame_rate) + '_object_h5'

    background_image_output_folder_name = \
        os.path.splitext(video_name)[0] + '_fr_' + \
        str(video_frame_rate) + '_background_jpg'

    ground_mask_image_folder_name = \
        os.path.splitext(video_name)[0] + \
        '_fr_' + str(video_frame_rate) + '_ground_mask_jpg'
    ground_image_output_folder_name = \
        os.path.splitext(video_name)[0] + '_fr_' \
        + str(video_frame_rate) + '_ground_jpg'
    ground_h5_output_folder_name = \
        os.path.splitext(video_name)[0] + '_fr_' \
        + str(video_frame_rate) + '_ground_h5'

    input_depth_image_folder_name = \
        os.path.splitext(video_name)[0] + \
        '_fr_' + str(video_frame_rate) + '_depth_exr'

    animation_transformations_file_suffix = \
        os.path.join(
            os.path.dirname(video_name),
            'ground_truth_files',
            'animation_transformations.txt')

    output_nvm_folder_name = \
        os.path.splitext(video_name)[0] + '_fr_' \
        + str(video_frame_rate) + '_depth_nvm'

    for possible_target_folder, dirs, files in os.walk(path_to_environment_output):

        if possible_target_folder.endswith(target_suffix):
            logger.info('target_folder: ' + possible_target_folder)

            path_to_model_output = os.path.dirname(possible_target_folder)

            # object files
            post_process_segmentation_output(
                model_idp=path_to_model_output,
                rendered_image_idn=rendered_image_folder_name,
                mask_image_idn=object_mask_image_folder_name,
                is_recursive_mask_idp=True,
                is_recursive_odp=True,
                image_odn=object_image_output_folder_name,
                h5_odn=object_h5_output_folder_name,
                lazy=lazy
            )

            # background files
            post_process_segmentation_output(
                model_idp=path_to_model_output,
                rendered_image_idn=rendered_image_folder_name,
                mask_image_idn=object_mask_image_folder_name,
                is_recursive_mask_idp=True,
                is_recursive_odp=False,
                image_odn=background_image_output_folder_name,
                h5_odn=None,
                invert_mask=True,
                lazy=lazy
            )

            # ground files
            post_process_segmentation_output(
                model_idp=path_to_model_output,
                rendered_image_idn=rendered_image_folder_name,
                mask_image_idn=ground_mask_image_folder_name,
                is_recursive_mask_idp=False,
                is_recursive_odp=False,
                image_odn=ground_image_output_folder_name,
                h5_odn=ground_h5_output_folder_name,
                lazy=lazy
            )
            if create_depth_files:
                # depth files
                post_process_depth_output(
                    path_to_model_output=path_to_model_output,
                    animation_transformations_file_suffix=animation_transformations_file_suffix,
                    input_depth_image_folder_name=input_depth_image_folder_name,
                    output_nvm_folder_name=output_nvm_folder_name)

    logger.info('perform_post_processing: Done')



if __name__ == '__main__':


    # Option 1
    # from Utility.Config import Config
    # from Blender.Trajectory_Renderer.Render_Trajectory import path_to_environment_blend_file
    # from Blender.Trajectory_Renderer.Render_Trajectory import path_to_parent_output_folder
    # environment_name = os.path.splitext(os.path.basename(path_to_environment_blend_file))[0]
    # path_to_environment_output = os.path.join(path_to_parent_output_folder, environment_name)
    #
    # output_config = Config(path_to_config_file='configs/output.cfg')
    # output_suffix = output_config.get_option_value_or_default_value('output_suffix', str, '')
    #
    # path_to_environment_output_with_suffix = path_to_environment_output + output_suffix
    # logger.vinfo('path_to_environment_output_with_suffix', path_to_environment_output_with_suffix)
    # perform_post_processing(path_to_environment_output_with_suffix, lazy=True)

    # Option 2

    parent_dp = os.path.dirname(os.path.realpath(__file__))
    post_processing_config = Config(path_to_config_file=os.path.join(
        parent_dp, 'config.cfg'))

    dp = post_processing_config.get_option_value('dataset_path', str)

    perform_post_processing(
        dp,
        create_depth_files=False)