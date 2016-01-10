

from osp.common import config
from osp.constants import redis_keys

from colour import Color


def text_count(text_id):

    """
    Get the total citation count for a text.

    Returns: int
    """

    count = config.redis.hget(
        redis_keys.OSP_WWW_COUNTS,
        text_id,
    )

    return int(count)


def text_score(text_id):

    """
    Get the teaching score for a text.

    Returns: float
    """

    pct = config.redis.hget(
        redis_keys.OSP_WWW_SCORES,
        text_id,
    )

    return round(float(pct)*100, 1)


def text_color(score, steps=100):

    """
    Convert a text score into a green -> red color.

    Args:
        steps (int) The number of gradient steps.

    Returns:
        str: A hex color.
    """

    r = Color('#f02424')
    g = Color('#29b730')

    gradient = list(r.range_to(g, steps))
    idx = round(score) - 1

    return gradient[idx].get_hex()
