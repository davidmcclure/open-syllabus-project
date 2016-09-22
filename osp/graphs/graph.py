

import os
import networkx as nx


class Graph:

    @classmethod
    def from_graphml(cls, path):

        """
        Hydrate an instance from a graphml file.

        Args:
            path (str)
        """

        graph = nx.read_graphml(os.path.abspath(path))

        return cls(graph)

    def __init__(self, graph=None):

        """
        Initialize the graph instance.

        Args:
            graph (nx.Graph)
        """

        self.graph = graph or nx.Graph()

    def write_graphml(self, path):

        """
        Serialize the graph as .graphml.

        Args:
            path (str)
        """

        nx.write_graphml(self.graph, path)
