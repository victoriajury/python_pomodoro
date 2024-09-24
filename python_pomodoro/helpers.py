import os
import pathlib

"""
Additional helper functions used by class function and methods.
"""


def get_image_from_resources(img_file_name: str) -> str:
    images_dir = pathlib.Path("resources/images/").resolve()
    img_path = os.path.join(images_dir, img_file_name)
    return img_path
