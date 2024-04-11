from IPYNBrenderer033.custom_exception import InvalidURLException
from IPYNBrenderer033.logger import logger
import urllib.request
from ensure import ensure_annotations
from IPython import display


@ensure_annotations
def is_valid(URL: str) -> bool:
    try:
        response_status = urllib.request.urlopen(URL).getcode()
        assert response_status == 200
        logger.debug(f"response_status: {response_status}")
        return True
    except Exception as e:
        logger.exception(e)
        return False


@ensure_annotations
def render_website(URL: str, width: str = "100%", height: str = "500") -> str:
    try:
        if is_valid(URL):
            response = display.IFrame(src=URL, width=width, height=height)
            display.display(response)
            return "successfully rendered website"
        else:
            raise InvalidURLException
    except Exception as e:
        raise e
