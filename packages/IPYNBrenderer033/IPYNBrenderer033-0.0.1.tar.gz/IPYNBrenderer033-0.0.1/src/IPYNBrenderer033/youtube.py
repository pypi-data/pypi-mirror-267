from IPython import display
from IPYNBrenderer033.custom_exception import InvalidURLException
from IPYNBrenderer033.logger import logger
from py_youtube import Data
from ensure import ensure_annotations


@ensure_annotations
def get_time_info(URL: str) -> int:
    def _verify_video_ID_len(video_ID, __expected_len=11):
        len_vid_id = len(video_ID)
        if len_vid_id != __expected_len:
            raise InvalidURLException(
                f"invalid length of video:{len_vid_id}  expected length is {__expected_len}"
            )

    try:
        split_val = URL.split("=")
        if len(split_val) > 3:
            raise InvalidURLException
        if "watch" in URL:
            if "&t" in URL:
                video_ID, time = split_val[-2][:-2], int(split_val[-1][:-1])
                _verify_video_ID_len(video_ID)
                logger.info(f"video starts at: {time}")
                return time
            else:
                video_ID, time = split_val[-1], 0
                _verify_video_ID_len(video_ID)
                logger.info(f"video starts at: {time}")
                return time
        else:
            if "=" in URL and "?t" in URL:
                video_ID, time = split_val[0].split("/")[-1][:-2], int(split_val[-1])
                _verify_video_ID_len(video_ID)
                logger.info(f"video starts at: {time}")
                return time
            else:
                video_ID, time = URL.split("/")[-1], 0
                _verify_video_ID_len(video_ID)
                logger.info(f"video starts at: {time}")
                return time
    except Exception:
        raise InvalidURLException


@ensure_annotations
def render_Youtube_video(URL: str, width: int = 780, height: int = 500) -> str:
    try:
        if URL is None:
            raise InvalidURLException("Url should not be none")
        data = Data(URL).data()
        if data["publishdate"] is not None:
            time = get_time_info(URL)
            video_ID = data["id"]
            embedded_URL = f"https://www.youtube.com/embed/{video_ID}?start={time}"
            logger.info(f"embedded_URL : {embedded_URL}")
            iframe = f"""<iframe width="{width}" height="{height}"
                        src="{embedded_URL}"
                        title="YouTube video player"
                        frameborder="0"
                        allow="accelerometer; autoplay; clipboard-write;
                        encrypted-media; gyroscope; picture-in-picture;
                        web-share" referrerpolicy="strict-origin-when-cross-origin"
                        allowfullscreen></iframe>"""
            display.display(display.HTML(iframe))
            return "successfullly rendered"
        else:
            raise InvalidURLException
    except Exception as e:
        raise e
