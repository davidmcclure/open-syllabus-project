

import os
import networkx as nx
import numpy as np
import math

from osp.common.config import config
from osp.common.utils import query_bar
from osp.citations.hlom.utils import prettify_field, sort_dict
from osp.citations.hlom.models.record import HLOM_Record
from osp.citations.hlom.models.citation import HLOM_Citation
from itertools import combinations
from clint.textui.progress import bar
from peewee import fn
from functools import lru_cache

from pgmagick import Image, Geometry, Color, TypeMetric, DrawableList, \
    DrawableCircle, DrawableFillColor, DrawableStrokeColor, \
    DrawableStrokeWidth, DrawableFillOpacity, DrawableText, \
    DrawablePointSize, DrawableLine, TypeMetric


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


    def add_edges(self, max_citations=50):

        """
        For each syllabus, register citation pairs as edges.

        Args:
            max_citations (int): Discard documents with > N citations.
        """

        # Aggregate the CNs.
        texts = (
            fn.array_agg(HLOM_Record.control_number)
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
            for cn1, cn2 in combinations(row.texts, 2):

                # If the edge exists, +1 the weight.
                if self.graph.has_edge(cn1, cn2):
                    self.graph[cn1][cn2]['weight'] += 1

                # Otherwise, initialize the edge.
                else: self.graph.add_edge(cn1, cn2, weight=1)


    def deduplicate(self):

        """
        Remove duplicate nodes.
        """

        seen = set()

        for cn in bar(self.graph.nodes()):

            # Pop out the HLOM record.
            text = HLOM_Record.get(HLOM_Record.control_number==cn)

            # If the node is a duplicate, remove it.
            if text.hash in seen: self.graph.remove_node(cn)
            else: seen.add(text.hash)


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


    def hydrate_nodes(self):

        """
        Hydrate node metadata.
        """

        for cn in bar(self.graph.nodes()):

            # Pop out the HLOM record.
            text = HLOM_Record.get(HLOM_Record.control_number==cn)

            # Prettify the title / author.
            title   = prettify_field(text.pymarc.title())
            author  = prettify_field(text.pymarc.author())

            self.graph.node[cn]['title'] = title
            self.graph.node[cn]['author'] = author


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


class GephiNetwork(Network):


    def weights(self):

        """
        Yields:
            float: The next edge weight.
        """

        for cn1, cn2, e in self.graph.edges_iter(data=True):
            yield e['weight'] if 'weight' in e else 1


    def xs(self):

        """
        Yields:
            float: The next X-axis coordinate.
        """

        for cn, node in self.graph.nodes_iter(data=True):
            yield node['viz']['position']['x']


    def ys(self):

        """
        Yields:
            float: The next Y-axis coordinate.
        """

        for cn, node in self.graph.nodes_iter(data=True):
            yield node['viz']['position']['y']


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


    def get_xy(self, cn, scale, size):

        """
        Get the X,Y position of a node.

        Args:
            cn (str): The text control number.
            scale (float): Pixels per coordinate unit.
            size (int): The render height/width.

        Returns:
            tuple: The (x, y) coordinate.
        """

        pos = self.graph.node[cn]['viz']['position']
        x =  (pos['x']*scale) + (size/2)
        y = -(pos['y']*scale) + (size/2)

        return (x, y)


    def position(self, scale, size):

        """
        Write (x,y) coordinates / radii onto the nodes.

        Args:
            scale (float): Pixels per coordinate unit.
            size (int): The render height/width.
        """

        for cn, n in bar(self.graph.nodes_iter(data=True),
                         expected_size=len(self.graph)):

            # Write the X,Y coordinate.
            x, y = self.get_xy(cn, scale, size)
            self.graph.node[cn]['x'] = x
            self.graph.node[cn]['y'] = y

            # Write the node radius.
            r = (n['viz']['size']*scale) / 2
            self.graph.node[cn]['r'] = r


    def render(self, path, scale=5, size=10000, font_size=14):

        """
        Render a PNG from the node coordinates.

        Args:
            path (str): The image path.
            scale (float): Pixels per coordinate unit.
            size (int): The height/width.
            font_size (int): The base font size.
        """

        image = Image(Geometry(size, size), Color('#11243a'))
        image.font(config['network']['font'])

        for cn, n in bar(self.graph.nodes_iter(data=True),
                         expected_size=len(self.graph)):

            x = n['x']
            y = n['y']
            r = n['r']

            label = ' '.join([
                n.get('title', ''),
                n.get('author', '')
            ])

            # Draw the node.
            dl = DrawableList()
            dl.append(DrawableFillColor('gray'))
            dl.append(DrawableStrokeColor('black'))
            dl.append(DrawableStrokeWidth(n['r']/15))
            dl.append(DrawableFillOpacity(0.9))
            dl.append(DrawableCircle(x, y, x+r, y+r))
            image.draw(dl)

            # TODO: Compute from size.
            image.fontPointsize(font_size)

            # Measure the width of the label.
            tm = TypeMetric()
            image.fontTypeMetrics(label, tm)
            width = tm.textWidth()

            # Draw the label.
            dl = DrawableList()
            dl.append(DrawablePointSize(font_size))
            dl.append(DrawableFillColor('white'))
            dl.append(DrawableText(x-(width/2), y, label))
            image.draw(dl)

        image.write(os.path.abspath(path))
