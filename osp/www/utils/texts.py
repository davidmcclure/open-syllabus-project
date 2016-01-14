

from colour import Color


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
