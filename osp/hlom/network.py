

import networkx as nx

from osp.citations.hlom.models.citation import HLOM_Citation
from playhouse.postgres_ext import ServerSide


class Network:


    @classmethod
    def from_gml(cls, file_path):

        """
        Hydrate the network from a GML file.

        Args:
            file_path (str)

        Returns:
            Network
        """

        pass


    def __init__(self, graph=None):

        """
        Set the graph instance.

        Args:
            graph (networkx.Graph)
        """

        self.graph = graph if graph else nx.Graph()


    def build(self):

        """
        Build the network from the citation table.
        """

        # Select cited HLOM records.
        nodes = (
            HLOM_Citation
            .select(HLOM_Citation.record)
            .distinct(HLOM_Citation.record)
        )

        # Add each record as a node.
        for node in ServerSide(nodes):

            title   = node.record.pymarc.title()
            author  = node.record.pymarc.author()

            self.graph.add_node(
                node.record.control_number,
                title=title,
                author=author
            )

        # add each cited HLOM record as a node DONE
        # for each syllabus, get all cited texts
        # for each pair of texts, +1 the edge weight


    def write_gml(self):

        """
        Serialize the graph as GML.
        """

        pass
