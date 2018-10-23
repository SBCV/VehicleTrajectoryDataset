
import os
from shutil import copyfile
from Dataset_Post_Processing.Segmentation_Post_Processing import post_process_segmentation_output
from Dataset_Post_Processing.Depth_Post_Processing import post_process_depth_output
from Dataset_Post_Processing.Video_Creation import create_video_from_images
from Dataset_Post_Processing.GT_Post_Processing import post_process_ground_truth

from Utility.Logging_Extension import logger
from Utility.Config import Config
from Utility.OS_Extension import delete_files_in_dir

def get_folder_stem(rendering_name, rendering_frame_rate):
    return os.path.splitext(rendering_name)[0] + '_fr_' + str(rendering_frame_rate)


def perform_image_post_processing(directory_path,
                                  remove_stereo_files,
                                  create_object_files,
                                  create_background_files,
                                  create_ground_files,
                                  create_depth_files,
                                  create_videos,
                                  lazy):

    target_suffix = '_frames_jpg'

    rendering_name = 'virtual.avi'
    stem = get_folder_stem(
        rendering_name=rendering_name,
        rendering_frame_rate=12.5)

    rendered_image_dn = stem + target_suffix

    object_mask_image_dn = stem + '_object_mask_jpg'
    object_image_odn = stem + '_object_jpg'
    object_h5_odn = stem + '_object_h5'

    background_image_odn = stem + '_background_jpg'

    ground_mask_image_dn = stem + '_ground_mask_jpg'
    ground_image_odn = stem + '_ground_jpg'
    ground_h5_odn = stem + '_ground_h5'

    input_depth_image_dn = stem + '_depth_exr'

    animation_transformations_file_suffix = \
        os.path.join(
            os.path.dirname(rendering_name),
            'ground_truth_files',
            'animation_transformations.txt')

    nvm_odn = \
        stem + '_depth_nvm'

    for possible_target_folder, dirs, files in os.walk(directory_path):

        if possible_target_folder.endswith(target_suffix):
            logger.info('target_folder: ' + possible_target_folder)

            model_path = os.path.dirname(possible_target_folder)

            if remove_stereo_files:
                delete_files_in_dir(
                    model_path,
                    ext=['.jpg', '.h5', '.exr'],
                    filter_str='right',
                    recursive=True)

            if create_object_files:
                post_process_segmentation_output(
                    model_idp=model_path,
                    rendered_image_idn=rendered_image_dn,
                    mask_image_idn=object_mask_image_dn,
                    is_recursive_mask_idp=True,
                    is_recursive_odp=True,
                    image_odn=object_image_odn,
                    h5_odn=object_h5_odn,
                    lazy=lazy)

            if create_background_files:
                post_process_segmentation_output(
                    model_idp=model_path,
                    rendered_image_idn=rendered_image_dn,
                    mask_image_idn=object_mask_image_dn,
                    is_recursive_mask_idp=True,
                    is_recursive_odp=False,
                    image_odn=background_image_odn,
                    h5_odn=None,
                    invert_mask=True,
                    lazy=lazy)

            if create_ground_files:
                post_process_segmentation_output(
                    model_idp=model_path,
                    rendered_image_idn=rendered_image_dn,
                    mask_image_idn=ground_mask_image_dn,
                    is_recursive_mask_idp=False,
                    is_recursive_odp=False,
                    image_odn=ground_image_odn,
                    h5_odn=ground_h5_odn,
                    lazy=lazy)

            if create_depth_files:
                # depth files
                post_process_depth_output(
                    model_idp=model_path,
                    animation_transformations_file_suffix=animation_transformations_file_suffix,
                    input_depth_image_folder_name=input_depth_image_dn,
                    output_nvm_folder_name=nvm_odn)

            if create_videos:
                # use left images only
                create_video_from_images(
                    model_idp=model_path,
                    rendered_image_idn=rendered_image_dn,
                    video_name=rendering_name,
                    filter_str='left',
                    lazy=lazy)

def perform_gt_post_processing(directory_path):

    gt_specific_dn = 'ground_truth_files'
    gt_general_idp = os.path.join(
        directory_path, 'general_ground_truth_files')

    for possible_target_folder, dirs, files in os.walk(directory_path):

        if os.path.basename(possible_target_folder) == gt_specific_dn:
            logger.info('gt_specific_dn: ' + possible_target_folder)

            post_process_ground_truth(
                gt_specific_dp=possible_target_folder,
                gt_general_idp=gt_general_idp
            )


def perform_post_processing(directory_path,
                            remove_stereo_files,
                            create_object_files,
                            create_background_files,
                            create_ground_files,
                            create_depth_files,
                            create_videos,
                            lazy):

    logger.info('perform_post_processing: ...')
    logger.vinfo('directory_path: ', directory_path)

    perform_image_post_processing(
        directory_path,
        remove_stereo_files,
        create_object_files,
        create_background_files,
        create_ground_files,
        create_depth_files,
        create_videos,
        lazy)

    perform_gt_post_processing(
        directory_path
    )


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
    example_config_path = os.path.join(parent_dp, 'Config', 'config_example.cfg')
    config_path = os.path.join(parent_dp, 'Config', 'config.cfg')

    if not os.path.isfile(config_path):
        copyfile(example_config_path, config_path)

    post_processing_config = Config(path_to_config_file=config_path)

    dp = post_processing_config.get_option_value(
        'dataset_path', str)
    lazy = post_processing_config.get_option_value(
        'lazy', bool)

    remove_stereo_files = post_processing_config.get_option_value(
        'remove_stereo_files', bool)

    create_object_files = post_processing_config.get_option_value(
        'create_object_files', bool)
    create_background_files = post_processing_config.get_option_value(
        'create_background_files', bool)
    create_ground_files = post_processing_config.get_option_value(
        'create_ground_files', bool)
    create_depth_files = post_processing_config.get_option_value(
        'create_depth_files', bool)

    create_videos = post_processing_config.get_option_value(
        'create_videos', bool)

    perform_post_processing(
        dp,
        remove_stereo_files,
        create_object_files,
        create_background_files,
        create_ground_files,
        create_depth_files=create_depth_files,
        create_videos=create_videos,
        lazy=lazy)
