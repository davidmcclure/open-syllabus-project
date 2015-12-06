

import os
import networkx as nx
import numpy as np
import math

from osp.common.config import config
from osp.common.utils import query_bar
from osp.hlom.utils import prettify_field, sort_dict
from osp.hlom.models import HLOM_Record
from osp.hlom.models import HLOM_Citation
from osp.hlom.models.hlom_node import HLOM_Node
from osp.hlom.models.hlom_edge import HLOM_Edge
from itertools import combinations
from clint.textui.progress import bar
from peewee import fn
from elasticsearch.helpers import bulk
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
            title       = prettify_field(text.marc.title())
            author      = prettify_field(text.marc.author())
            publisher   = prettify_field(text.marc.publisher())
            pubyear     = prettify_field(text.marc.pubyear())

            self.graph.node[cn]['title']        = title or ''
            self.graph.node[cn]['author']       = author or ''
            self.graph.node[cn]['publisher']    = publisher or ''
            self.graph.node[cn]['pubyear']      = pubyear or ''


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


    es_index = 'network'
    es_doc_type = 'node'

    es_mapping = {
        '_id': {
            'index': 'not_analyzed',
            'store': True
        },
        'properties': {
            'title': {
                'type': 'string'
            },
            'author': {
                'type': 'string'
            },
            'publisher': {
                'type': 'string'
            },
            'pubyear': {
                'type': 'string'
            },
            'location': {
                'type': 'geo_point'
            },
            'degree': {
                'type': 'integer'
            }
        }
    }


    @classmethod
    def es_create(cls):

        """
        Set the Elasticsearch mapping.
        """

        config.es.indices.create(cls.es_index, {
            'mappings': { cls.es_doc_type: cls.es_mapping }
        })


    @classmethod
    def es_delete(cls):

        """
        Delete the index.
        """

        if config.es.indices.exists(cls.es_index):
            config.es.indices.delete(cls.es_index)


    @classmethod
    def es_count(cls):

        """
        Count the number of documents.

        Returns:
            int: The number of docs.
        """

        r = config.es.count(cls.es_index, cls.es_doc_type)
        return r['count']


    @classmethod
    def es_reset(cls):

        """
        Clear and recreate the index.
        """

        cls.es_delete()
        cls.es_create()


    def es_stream_docs(self):

        """
        Generate Elasticsearch documents.
        """

        for cn, n in bar(self.graph.nodes_iter(data=True),
                         expected_size=len(self.graph)):

            yield {

                '_id':          cn,
                'title':        n.get('title'),
                'author':       n.get('author'),
                'publisher':    n.get('publisher'),
                'pubyear':      n.get('pubyear'),
                'degree':       n.get('Degree'),

                'location': {
                    'lon': n['x'],
                    'lat': n['y']
                }

            }


    def es_insert(self):

        """
        Insert Elasticsearch documents.
        """

        # Batch-insert the documents.
        bulk(
            config.es,
            self.es_stream_docs(),
            raise_on_exception=False,
            doc_type=self.es_doc_type,
            index=self.es_index
        )

        # Commit the index.
        config.es.indices.flush(self.es_index)


    def pg_insert_nodes(self):

        """
        Insert Postgres nodes.
        """

        for cn, n in bar(self.graph.nodes_iter(data=True),
                         expected_size=len(self.graph)):

            # Insert the node.
            HLOM_Node.create(control_number=cn, node=n)


    def pg_insert_edges(self):

        """
        Insert Postgres edges.
        """

        size = nx.number_of_edges(self.graph)

        for cn1, cn2, e in bar(self.graph.edges_iter(data=True),
                               expected_size=size):

            # Pop out the nodes.
            n1 = HLOM_Node.get(HLOM_Node.control_number==cn1)
            n2 = HLOM_Node.get(HLOM_Node.control_number==cn2)

            HLOM_Edge.create(
                source=n1,
                target=n2,
                weight=e.get('weight', 1)
            )

            HLOM_Edge.create(
                source=n2,
                target=n1,
                weight=e.get('weight', 1)
            )


    def weights(self):

        """
        Yields:
            float: The next edge weight.
        """

        for cn1, cn2, e in self.graph.edges_iter(data=True):
            yield e.get('weight', 1)


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


    def get_xy(self, cn, scale, width):

        """
        Get the X,Y position of a node.

        Args:
            scale (float): Pixels per coordinate unit.
            width (int): The render height/width.

        Returns:
            tuple: The (x, y) coordinate.
        """

        pos = self.graph.node[cn]['viz']['position']
        x =  (pos['x']*scale) + (width/2)
        y = -(pos['y']*scale) + (width/2)

        return (x, y)


    def render(self, path, scale=5, width=10000, min_size=10, max_size=200,
               min_fsize=14, max_fsize=200, bg_color='#003059'):

        """
        Render a PNG from the node coordinates.

        Args:
            path (str): The image path.
            scale (float): Pixels per coordinate unit.
            width (int): The height/width, in pixels.
            min_size (int): The min node size.
            max_size (int): The max node size.
            min_fsize (int): The min font size.
            max_fsize (int): The max font size.
        """

        # Initialize the canvas, set font.
        image = Image(Geometry(width, width), Color(bg_color))

        # Set the label font.
        image.font(config['network']['font'])

        for cn, n in bar(self.graph.nodes_iter(data=True),
                         expected_size=len(self.graph)):

            # Get (x,y) / radius.
            x, y = self.get_xy(cn, scale, width)
            r = (n['viz']['size']*scale) / 2

            # Index the coordinates.
            self.graph.node[cn]['x'] = x
            self.graph.node[cn]['y'] = y
            self.graph.node[cn]['r'] = r

            # Get the node label.
            label = ', '.join([
                n.get('title', ''),
                n.get('author', '')
            ])

            # Get the node color.
            color = '#%02x%02x%02x' % (
                n['viz']['color']['r'],
                n['viz']['color']['g'],
                n['viz']['color']['b']
            )

            # Draw the node.
            dl = DrawableList()
            dl.append(DrawableFillColor(color))
            dl.append(DrawableStrokeColor('black'))
            dl.append(DrawableStrokeWidth(n['r']/15))
            dl.append(DrawableFillOpacity(0.9))
            dl.append(DrawableCircle(x, y, x+r, y+r))
            image.draw(dl)

            # Compute the font size.
            ratio = (n['viz']['size']-min_size) / (max_size-min_size)
            fsize = min_fsize + (ratio*(max_fsize-min_fsize))
            image.fontPointsize(fsize)

            # Measure the width of the label.
            tm = TypeMetric()
            image.fontTypeMetrics(label, tm)
            tw = tm.textWidth()

            # Draw the label.
            dl = DrawableList()
            dl.append(DrawablePointSize(fsize))
            dl.append(DrawableFillColor('white'))
            dl.append(DrawableText(x-(tw/2), y, label))
            image.draw(dl)

        image.write(os.path.abspath(path))
