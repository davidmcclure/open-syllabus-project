

import os
import networkx as nx
import numpy as np
import math

from osp.common.utils import query_bar
from osp.citations.hlom.utils import prettify_field, sort_dict
from osp.citations.hlom.models.record import HLOM_Record
from osp.citations.hlom.models.citation import HLOM_Citation
from pgmagick import Image, Geometry, Color, DrawableCircle
from itertools import combinations
from clint.textui.progress import bar
from peewee import fn
from functools import lru_cache


class Network:


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


    def invert_edge_weights(self):

        """
        Adjust edge weights to be real values between 0 and 1, where "close"
        nodes have low weights.
        """

        max_weight = np.log(self.max_weight)

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


    def trim_unconnected_components(self):

        """
        Remove unconnected components.
        """

        subgraphs = sorted(
            nx.connected_component_subgraphs(self.graph),
            key=len,
            reverse=True
        )

        self.graph = subgraphs[0]


    # TODO|dev


    def degree_centrality(self, depth):

        """
        Print title -> degree centrality.

        Args:
            depth (int): The number of texts to display.
        """

        dc = sort_dict(nx.degree_centrality(self.graph))

        results = []
        for nid, d in list(dc.items())[:depth]:
            results.append((nid, self.graph.node[nid]['title'], d))

        return results


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

        results = []
        for nid, d in sort_dict(nearest, False).items():
            results.append((d, self.graph.node[nid]['title']))

        return results


    def neighbors(self, nid):

        """
        Given a HLOM record ID, get all neighboring nodes.

        Args:
            nid (int): The ID of the source node.
        """

        tids = self.graph.neighbors(nid)

        results = []
        for tid in tids:
            edge = self.graph.edge[nid][tid]
            node = self.graph.node[tid]
            results.append((edge['weight'], node['title']))

        return sorted(results, key=lambda x: x[0], reverse=True)


class GephiNetwork(Network):


    def weights(self):

        """
        Yields:
            float: The next edge weight.
        """

        for e in self.graph.edges_iter(data=True):
            yield e[2]['weight'] if 'weight' in e[2] else 1


    def xs(self):

        """
        Yields:
            float: The next X-axis coordinate.
        """

        for n in self.graph.nodes_iter(data=True):
            yield n[1]['viz']['position']['x']


    def ys(self):

        """
        Yields:
            float: The next Y-axis coordinate.
        """

        for n in self.graph.nodes_iter(data=True):
            yield n[1]['viz']['position']['y']


    @property
    @lru_cache()
    def max_weight(self):

        """
        Returns:
            int: The heaviest edge weight.
        """

        return max(list(self.weights()))


    @property
    @lru_cache()
    def min_x(self):

        """
        Returns:
            float: The minimum X-axis coordinate.
        """

        return min(list(self.xs()))


    @property
    @lru_cache()
    def max_x(self):

        """
        Returns:
            float: The maximum X-axis coordinate.
        """

        return max(list(self.xs()))


    @property
    @lru_cache()
    def min_y(self):

        """
        Returns:
            float: The minimum Y-axis coordinate.
        """

        return min(list(self.ys()))


    @property
    @lru_cache()
    def max_y(self):

        """
        Returns:
            float: The maximum Y-axis coordinate.
        """

        return max(list(self.ys()))


    @property
    @lru_cache()
    def height(self):

        """
        Returns:
            int: The Y-axis coordinate range.
        """

        return math.ceil(self.max_y - self.min_y)


    @property
    @lru_cache()
    def width(self):

        """
        Returns:
            int: The X-axis coordinate range.
        """

        return math.ceil(self.max_x - self.min_x)


    def draw_png(self, path, ppu=10, size=10000, radius=5):

        """
        Render a PNG from the node coordinates.

        Args:
            path (str): The image path.
            ppu (float): Pixels per coordinate unit.
            size (int): The height/width.
            radius (int): The node radius.
        """

        image = Image(Geometry(size, size), Color('white'))

        for id, node in bar(self.graph.nodes_iter(data=True),
                        expected_size=len(self.graph)):

            # Flip the Y-axis to document-space.
            x =  (node['viz']['position']['x']*ppu) + (size/2)
            y = -(node['viz']['position']['y']*ppu) + (size/2)

            # Draw the node.
            circle = DrawableCircle(x, y, x+radius, y+radius)
            image.draw(circle)

        image.write(os.path.abspath(path))
