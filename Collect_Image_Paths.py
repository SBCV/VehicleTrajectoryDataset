import os

def get_image_paths_in_folder(image_folder, ext='.jpg'):
    image_paths = [os.path.join(image_folder, file_name)
                   for file_name in os.listdir(image_folder)
                   if (os.path.isfile(os.path.join(image_folder, file_name))
                   and os.path.splitext(file_name)[1] == ext)]
    return image_paths


