import logging
import requests
from pydantic import UUID4

from app.core.config import ML_CALLER_URL

logger = logging.getLogger("genicons").getChild("send")


async def caller(
    image_bytes: bytes,
    product_id: UUID4,
):
    try:
        logger.debug("genicon_caller(): start")

        datas = {'product_id': product_id}
        files = {'image': (f'{product_id}.jpg', image_bytes, 'image/jpeg')}

        response = requests.post(
            ML_CALLER_URL,
            data=datas,
            files=files,
        )

        logger.info(f"ml_caller() {response.status_code}: {response.content}")

    except Exception as e:
        logger.error(e)
    finally:
        logger.debug("genicon_caller(): done")
