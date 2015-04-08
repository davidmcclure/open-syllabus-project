

import networkx as nx

from osp.citations.hlom.models.record import HLOM_Record
from osp.citations.hlom.models.citation import HLOM_Citation
from itertools import combinations
from playhouse.postgres_ext import ServerSide
from clint.textui.progress import bar
from peewee import fn


def query_bar(q):
    return bar(ServerSide(q), expected_size=q.count())


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


    def add_nodes(self):

        """
        Register unique HLOM records as nodes.
        """

        # Select cited HLOM records.
        texts = (
            HLOM_Citation
            .select(HLOM_Citation.record)
            .distinct(HLOM_Citation.record)
        )

        # Add each record as a node.
        for row in query_bar(texts):

            title  = row.record.pymarc.title()
            author = row.record.pymarc.author()

            self.graph.add_node(
                row.record.control_number,
                title=title,
                author=author
            )


    def add_edges(self, max_texts=20):

        """
        For each syllabus, register citation pairs as edges.

        Args:
            max_texts (int)
        """

        # Aggregate the CNs.
        cns = (
            fn.array_agg(HLOM_Record.control_number)
            .coerce(False)
            .alias('texts')
        )

        # Select syllabi and cited CNs.
        documents = (
            HLOM_Citation
            .select(HLOM_Citation.document, cns)
            .join(HLOM_Record)
            .distinct(HLOM_Citation.document)
            .group_by(HLOM_Citation.document)
        )

        print(documents.sql())

        for row in query_bar(documents):

            if len(row.texts) > max_texts:
                continue

            for cn1, cn2 in combinations(row.texts, 2):

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
