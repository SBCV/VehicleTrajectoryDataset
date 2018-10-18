import numpy as np
from PIL import Image, ImageFile
import os
from Utility.Logging_Extension import logger
from Utility.File_Handler.H5_File_Handler import H5FileHandler
from Utility.OS_Extension import mkdir_safely, makedirs_safely
from Collect_Image_Paths import get_image_paths_in_folder


def create_output_for_folder(path_to_model_output,
                             frames_jpg_list,
                             mask_image_ifp,
                             masked_jpg_image_ofp,
                             invert_mask,
                             output_h5_folder_name,
                             lazy):

    # Required to avoid "IOError: broken data stream when reading image file" error
    ImageFile.LOAD_TRUNCATED_IMAGES = True

    if not output_h5_folder_name is None:
        output_h5_folder_path = os.path.join(
            path_to_model_output, output_h5_folder_name)
        makedirs_safely(output_h5_folder_path)
        logger.vinfo('output_h5_folder_name', output_h5_folder_name)

    input_mask_list = get_image_paths_in_folder(mask_image_ifp)

    for frame_jpg_path, input_object_mask_jpg_path in zip(
            frames_jpg_list, input_mask_list):
        frame_jpg_name = os.path.basename(frame_jpg_path)
        output_mask_jpg_path = os.path.join(
            masked_jpg_image_ofp, frame_jpg_name)

        jpg_file_missing = not os.path.isfile(output_mask_jpg_path)

        if output_h5_folder_name is None:
            h5_file_missing = False
        else:
            output_h5_file_path = os.path.join(
                output_h5_folder_path, os.path.splitext(frame_jpg_name)[0] + '.h5')
            h5_file_missing = not os.path.isfile(output_h5_file_path)

        if jpg_file_missing or h5_file_missing or not lazy:
            frame_jpg_array = np.asarray(
                Image.open(frame_jpg_path).convert('RGB'))

            # The masks contain values between 0 and 255
            # L == grey scale
            input_mask_array = np.asarray(
                Image.open(input_object_mask_jpg_path).convert('L'))

            if jpg_file_missing:
                output_mask_jpg_array = frame_jpg_array.copy()
                # This works even output_mask_jpg_array has 3 and object_mask_jpg has 1 channel
                if invert_mask:
                    output_mask_jpg_array[input_mask_array >= 127] = (255, 255, 255)
                else:
                    # set all non target pixels to white
                    output_mask_jpg_array[input_mask_array < 127] = (255, 255, 255)
                output_mask_jpg_image = Image.fromarray(output_mask_jpg_array)
                output_mask_jpg_image.save(output_mask_jpg_path)
                logger.info('output_mask_jpg_path: ' + output_mask_jpg_path)

            if h5_file_missing:
                ground_mask_array_0_255 = np.copy(input_mask_array)
                if invert_mask:
                    ground_mask_array_0_255[input_mask_array >= 127] = 0
                    ground_mask_array_0_255[input_mask_array < 127] = 255
                else:
                    ground_mask_array_0_255[input_mask_array < 127] = 0
                    ground_mask_array_0_255[input_mask_array >= 127] = 255
                H5FileHandler.write_h5(output_h5_file_path, ground_mask_array_0_255)
                logger.info('output_h5_file_path: ' + output_h5_file_path)


def post_process_segmentation_output(model_idp,
                                     rendered_image_idn,
                                     mask_image_idn,
                                     is_recursive_mask_idp,
                                     is_recursive_odp,
                                     image_odn,
                                     h5_odn=None,
                                     invert_mask=False,
                                     lazy=True):


    logger.info('post_process_segmentation_output: ...')
    # Input paths
    rendered_image_idp = os.path.join(
        model_idp, rendered_image_idn)
    mask_image_idp = os.path.join(
        model_idp, mask_image_idn)

    # Output paths
    masked_jpg_image_odp = os.path.join(
        model_idp, image_odn)
    mkdir_safely(masked_jpg_image_odp)

    logger.vinfo('rendered_image_idp', rendered_image_idp)
    logger.vinfo('mask_image_idp', mask_image_idp)
    logger.vinfo('masked_jpg_image_odp', masked_jpg_image_odp)
    logger.vinfo('is_recursive_mask_idp', is_recursive_mask_idp)

    frames_jpg_list = get_image_paths_in_folder(rendered_image_idp)
    logger.info('Found ' + str(len(frames_jpg_list)) + ' images')

    if is_recursive_mask_idp:

        dir_names = [ele for ele in os.listdir(mask_image_idp) if os.path.isdir(os.path.join(mask_image_idp, ele))]

        for dir_n in dir_names:
            mask_image_sub_ifp = os.path.join(mask_image_idp, dir_n)

            if is_recursive_odp:  # For object segmentations
                actual_masked_jpg_image_odp = os.path.join(masked_jpg_image_odp, dir_n)
            else:  # For background segmentations
                # TODO This works only when there is only one target object in the scene
                actual_masked_jpg_image_odp = os.path.join(masked_jpg_image_odp)

            mkdir_safely(actual_masked_jpg_image_odp)

            if h5_odn is not None:
                h5_sub_odn = os.path.join(h5_odn, dir_n)
            else:
                h5_sub_odn = None

            create_output_for_folder(
                model_idp,
                frames_jpg_list,
                mask_image_sub_ifp,
                actual_masked_jpg_image_odp,
                invert_mask,
                h5_sub_odn,
                lazy)

    else:   # For ground segmentations
        create_output_for_folder(
            model_idp,
            frames_jpg_list,
            mask_image_idp,
            masked_jpg_image_odp,
            invert_mask,
            h5_odn,
            lazy)

    logger.info('post_process_segmentation_output: Done')




