

import math

from colour import Color


class Hit:

    def __init__(self, hit):

        """
        Set the raw Elasticsearch hit.

        Args:
            hit (dict)
        """

        self.hit = hit

    def field(self, key, delimiter=', '):

        """
        Get a document field.

        Args:
            key (str)

        Returns: str
        """

        value = self.hit['_source'][key]

        if type(value) == list:
            return delimiter.join(value)

        else:
            return value

    def path(self):

        """
        Get the URL path.

        Returns: str
        """

        return '/text/{0}'.format(self.hit['_id'])

    def sort(self):

        """
        Get the sort value.

        Returns: int
        """

        return int(self.hit['sort'][0])

    def color(self, steps=100):

        """
        Get a green -> red scoring color.

        Args:
            steps (int): The number of gradient steps.

        Returns:
            str: A hex color.
        """

        low  = Color('#000000')
        high = Color('#29b730')

        gradient = list(low.range_to(high, steps))
        idx = round(self.field('score')*(steps-1))

        return gradient[idx].get_hex()
