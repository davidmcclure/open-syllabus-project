

import os
import networkx as nx
import numpy as np

from osp.common.utils import query_bar
from osp.citations.hlom.utils import prettify_field, sort_dict
from osp.citations.hlom.models.record import HLOM_Record
from osp.citations.hlom.models.citation import HLOM_Citation
from itertools import combinations
from clint.textui.progress import bar
from peewee import fn


class Network:


    @classmethod
    def from_gml(cls, path):

        """
        Hydrate the network from a .gml file.

        Args:
            path (str)

        Returns:
            Network
        """

        graph = nx.read_gml(os.path.abspath(path))
        return cls(graph)


    @classmethod
    def from_gexf(cls, path):

        """
        Hydrate the network from a .gexf file.

        Args:
            path (str)

        Returns:
            Network
        """

        graph = nx.read_gexf(os.path.abspath(path))
        return cls(graph)


    def __init__(self, graph=None):

        """
        Set the graph instance.

        Args:
            graph (networkx.Graph)
        """

        self.graph = graph if graph else nx.Graph()


    def write_gml(self, path):

        """
        Serialize the graph as .gml.

        Args:
            path (str)
        """

        nx.write_gml(self.graph, path)


    def write_gexf(self, path):

        """
        Serialize the graph as .gexf.

        Args:
            path (str)
        """

        nx.write_gexf(self.graph, path)


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


    def max_edge_weight(self):

        """
        What is the highest edge weight in the network?

        Returns:
            int: The max edge weight.
        """

        edges = self.graph.edges_iter(data=True)
        weights = [e[2]['weight'] for e in edges]
        return max(weights)


    def normalize_edge_weights(self):

        """
        Adjust edge weights to be real values between 0 and 1, where "close"
        nodes have low weights.
        """

        max_weight = np.log(self.max_edge_weight())

        for e in self.graph.edges_iter(data=True):

            # Normalize against the max.
            w = 1-(np.log(e[2]['weight'])/max_weight)

            # Set the new value.
            self.graph.edge[e[0]][e[1]]['weight'] = w


    def hydrate_labels(self):

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


    def deduplicate(self):

        """
        Remove duplicate nodes.
        """

        seen = set()

        for nid in bar(self.graph.nodes()):

            # Pop out the HLOM record.
            text = HLOM_Record.get(HLOM_Record.id==nid)

            # If the node is a duplicate, remove it.
            if text.hash in seen: self.graph.remove_node(nid)
            else: seen.add(text.hash)


    # TODO|dev


    def degree_centrality(self, depth):

        """
        Print title -> degree centrality.

        Args:
            depth (int): The number of texts to display.
        """

        dc = sort_dict(nx.degree_centrality(self.graph))

        return [(nid, self.graph.node[nid]['title'], d)
                for nid, d in list(dc.items())[:depth]]


    def mlt(self, nid, cutoff=None):

        """
        Given a HLOM record ID, get the N "nearest" records.

        Args:
            nid (int): The ID of the source node.
            cutoff (int): Depth to stop the search.
        """

        nearest = nx.single_source_dijkstra_path_length(
            self.graph, nid, cutoff
        )

        for nid, d in sort_dict(nearest, False).items():
            print(d, self.graph.node[nid]['title'])
