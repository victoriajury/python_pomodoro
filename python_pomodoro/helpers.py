import os
import pathlib


def get_image_from_resources(img_file_name: str) -> str:
    images_dir = pathlib.Path("resources/images/").resolve()
    img_path = os.path.join(images_dir, img_file_name)
    return img_path
