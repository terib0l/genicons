import functools
import numpy as np
import tensorflow as tf
import matplotlib.pylab as plt
from PIL import Image, ImageDraw


def crop_center(
    image
):
    """
    Returns a cropped square image.
    """
    shape = image.shape
    new_shape = min(shape[1], shape[2])
    offset_y = max(shape[1] - shape[2], 0) // 2
    offset_x = max(shape[2] - shape[1], 0) // 2
    image = tf.image.crop_to_bounding_box(
        image, offset_y, offset_x, new_shape, new_shape)
    return image


@functools.lru_cache(maxsize=None)
def load_image(
    image: bytes,
    image_size: tuple = (256, 256),
    preserve_aspect_ratio: bool = True
):
    """
    Loads and preprocesses images.
    """
    img = plt.imread(image, format='jpeg').astype(np.float32)[np.newaxis, ...]
    if img.max() > 1.0:
      img = img / 255.
    if len(img.shape) == 3:
      img = tf.stack([img, img, img], axis=-1)
    img = crop_center(img)
    img = tf.image.resize(img, image_size, preserve_aspect_ratio=True)
    return img


def circle_mask(
    image: Image.Image
):
    offset = 10

    mask = Image.new("L", image.size)
    draw = ImageDraw.Draw(mask)

    draw.ellipse(
        [
            (offset, offset),
            (image.size[0] - offset, image.size[1] - offset)
        ],
        255
    )
    del draw

    image.putalpha(mask)
    return image


def rounded_square_mask(
    image: Image.Image
):
    rx = 100
    ry = 100
    fillcolor = "#ffffff"

    mask = Image.new("L", image.size)
    draw = ImageDraw.Draw(mask)

    draw.rectangle(
        (0,ry)+(mask.size[0]-1,mask.size[1]-1-ry),
        fill=fillcolor
    )
    draw.rectangle(
        (rx,0)+(mask.size[0]-1-rx,mask.size[1]-1),
        fill=fillcolor
    )
    draw.pieslice(
        (0, 0)+(rx*2, ry*2),
        180,
        270,
        fill=fillcolor
    )
    draw.pieslice(
        (0, mask.size[1]-1-ry*2)+(rx*2, mask.size[1]-1),
        90,
        180,
        fill=fillcolor
    )
    draw.pieslice(
        (mask.size[0]-1-rx*2, mask.size[1]-1-ry*2)+(mask.size[0]-1, mask.size[1]-1),
        0,
        180,
        fill=fillcolor
    )
    draw.pieslice(
        (mask.size[0]-1-rx*2, 0)+(mask.size[0]-1, ry*2),
        270,
        360,
        fill=fillcolor
    )
    del draw

    image.putalpha(mask)
    return image
