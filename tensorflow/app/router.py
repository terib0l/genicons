import io
import tensorflow as tf
import tensorflow_hub as hub
from pydantic import UUID4
from sqlalchemy.orm import Session
from fastapi import APIRouter, UploadFile, File, Depends, Form

from app.config import STYLE_IMAGE_URL
from app.db import (
    get_db,
    create_circle_icon,
    create_rounded_square_icon
)
from app.util import (
    load_image,
    circle_mask,
    rounded_square_mask
)

router = APIRouter()

@router.post("/generate/icon")
async def generate_icon(
    product_id: UUID4 = Form(...),
    image: UploadFile = File(...),
    session: Session = Depends(get_db),
):
    """
    Create Icon-like Image by Style Transfer

    Args:

        product_id: Form(uuid4)
        image: Form(jpg)

    Return:

        {"status": "success"/"error"}
    """
    try:
        # Input image
        fp = io.BytesIO(await image.read())
        content_image = load_image(fp, (256, 256))

        # Base-style image
        with open(STYLE_IMAGE_URL, 'rb') as style_image:
            fp = io.BytesIO(style_image.read())
        style_image = load_image(fp, (256, 256))
        style_image = tf.nn.avg_pool(style_image, ksize=[3,3], strides=[1,1], padding='SAME')

        hub_handle = 'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2'
        hub_module = hub.load(hub_handle)

        outputs = hub_module(tf.constant(content_image), tf.constant(style_image))
        stylized_image = outputs[0][0]

        result = tf.keras.preprocessing.image.array_to_img(stylized_image)
        # result.save('./result.jpg')

        circle_result = circle_mask(result)
        create_circle_icon(session, circle_result, product_id)
        # circle_result.save('./circle_result.png')

        rounded_square_result = rounded_square_mask(result)
        create_rounded_square_icon(session, rounded_square_result, product_id)
        # rounded_square_result.save('./rounded_square_result.png')

        return {'status': 'success'}

    except Exception as e:
        print(e)
        return {'status': 'error'}

