

import networkx as nx

from osp.citations.hlom.models.citation import HLOM_Citation
from itertools import combinations
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
        texts = (
            HLOM_Citation
            .select(HLOM_Citation.record)
            .distinct(HLOM_Citation.record)
        )

        # Add each record as a node.
        for row in ServerSide(texts):

            title  = row.record.pymarc.title()
            author = row.record.pymarc.author()

            self.graph.add_node(
                row.record.control_number,
                title=title,
                author=author
            )

        syllabi = (
            HLOM_Citation
            .select(HLOM_Citation.document)
            .distinct(HLOM_Citation.document)
        )

        for row in ServerSide(syllabi):

            texts = (
                HLOM_Citation
                .select(HLOM_Citation.record)
                .where(HLOM_Citation.document==row.document)
            )

            for t1, t2 in combinations(list(texts), 2):

                cn1 = t1.record.control_number
                cn2 = t2.record.control_number

                # If the edge exists, +1 the weight.
                if self.graph.has_edge(cn1, cn2):
                    self.graph[cn1][cn2]['weight'] += 1

                # Otherwise, initialize the edge.
                else: self.graph.add_edge(cn1, cn2, weight=1)


    def write_gml(self):

        """
        Serialize the graph as GML.
        """

        pass
