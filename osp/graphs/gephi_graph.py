

import networkx as nx
import os
import math

from cached_property import cached_property


class Gephi_Graph:


    def __init__(self, path):

        """
        Read the Gephi .graphml file.

        Args:
            path (str)
        """

        self.graph = nx.read_graphml(os.path.abspath(path))


    def xs(self):

        """
        Yields: The next X-axis coordinate.
        """

        for cn, node in self.graph.nodes_iter(data=True):
            yield node['x']


    def ys(self):

        """
        Yields: The next Y-axis coordinate.
        """

        for cn, node in self.graph.nodes_iter(data=True):
            yield node['y']


    @cached_property
    def min_x(self):

        """
        Returns: The minimum X-axis coordinate.
        """

        return min(list(self.xs()))


    @cached_property
    def max_x(self):

        """
        Returns: The maximum X-axis coordinate.
        """

        return max(list(self.xs()))


    @cached_property
    def min_y(self):

        """
        Returns: The minimum Y-axis coordinate.
        """

        return min(list(self.ys()))


    @cached_property
    def max_y(self):

        """
        Returns: The maximum Y-axis coordinate.
        """

        return max(list(self.ys()))


    @cached_property
    def height(self):

        """
        Returns: The Y-axis coordinate range.
        """

        return math.ceil(self.max_y - self.min_y)


    @cached_property
    def width(self):

        """
        Returns: The X-axis coordinate range.
        """

        return math.ceil(self.max_x - self.min_x)
