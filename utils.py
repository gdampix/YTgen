from PIL import Image
import numpy as np


def remove_bg_color(image, rgba):
    image_data = np.array(image.convert('RGBA'))        # rgba array from image
    pixels = image_data.view(dtype=np.uint32)[...,0]  # pixels as rgba uint32
    image_data[...,3] = np.where(pixels == np.uint32(rgba), np.uint8(0), np.uint8(255))  # set alpha channel
    return Image.fromarray(image_data)