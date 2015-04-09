

import os
import networkx as nx

from osp.common.utils import query_bar
from osp.citations.hlom.models.record import HLOM_Record
from osp.citations.hlom.models.citation import HLOM_Citation
from osp.citations.hlom.utils import prettify_field
from itertools import combinations
from clint.textui.progress import bar
from peewee import fn


class Network:


    @classmethod
    def from_gml(cls, path):

        """
        Hydrate the network from a GML file.

        Args:
            path (str)

        Returns:
            Network
        """

        graph = nx.read_gml(os.path.abspath(path))
        return cls(graph)


    def __init__(self, graph=None):

        """
        Set the graph instance.

        Args:
            graph (networkx.Graph)
        """

        self.graph = graph if graph else nx.Graph()


    def add_edges(self, max_citations=20):

        """
        For each syllabus, register citation pairs as edges.

        Args:
            max_citations (int): Discard documents with > N citations.
        """

        # Aggregate the CNs.
        texts = (
            fn.array_agg(HLOM_Record.id)
            .coerce(False)
            .alias('texts')
        )

        # Select syllabi and cited CNs.
        documents = (
            HLOM_Citation
            .select(HLOM_Citation.document, texts)
            .join(HLOM_Record)
            .having(fn.count(HLOM_Record.id) <= max_citations)
            .distinct(HLOM_Citation.document)
            .group_by(HLOM_Citation.document)
        )

        for row in query_bar(documents):
            for id1, id2 in combinations(row.texts, 2):

                # If the edge exists, +1 the weight.
                if self.graph.has_edge(id1, id2):
                    self.graph[id1][id2]['weight'] += 1

                # Otherwise, initialize the edge.
                else: self.graph.add_edge(id1, id2, weight=1)


    def hydrate_nodes(self):

        """
        Hydrate node labels.
        """

        for nid in bar(self.graph.nodes()):

            # Pop out the HLOM record.
            text = HLOM_Record.get(HLOM_Record.id==nid)

            # Prettify "[title] [author]".
            label = ', '.join([
                prettify_field(text.pymarc.title()),
                prettify_field(text.pymarc.author())
            ])

            self.graph.node[nid]['title'] = label


    def write_gml(self, path):

        """
        Serialize the graph as GML.

        Args:
            path (str)
        """

        nx.write_gml(self.graph, path)
