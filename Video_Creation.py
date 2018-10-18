import os
from Utility.FFMPEG_Scripts.Video_From_Image_Creator import VideoFromImageCreator
from Collect_Image_Paths import get_image_paths_in_folder

def create_video_from_images(model_idp, rendered_image_idn, video_name, filter_str, lazy):

    rendered_image_idp = os.path.join(
         model_idp, rendered_image_idn)
    # frames_jpg_list = get_image_paths_in_folder(rendered_image_idp)

    path_to_output_video_and_name = os.path.join(model_idp, video_name)

    video_from_image_creator = VideoFromImageCreator()
    video_from_image_creator.create_video_from_images(
        path_to_images=rendered_image_idp,
        video_ofp=path_to_output_video_and_name,
        filter_str=filter_str,
        add_ignore_file=False,
        lazy=lazy)
