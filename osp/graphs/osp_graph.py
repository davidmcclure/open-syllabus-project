

from osp.common.utils import query_bar
from osp.citations.models import Text, Citation, Text_Index
from osp.corpus.models import Document

import networkx as nx
from itertools import combinations
from peewee import fn
from clint.textui import progress


class OSP_Graph:


    def __init__(self):

        """
        Initialize the graph instance.
        """

        self.graph = nx.Graph()


    def add_edges(self, text_cap=20):

        """
        For each syllabus, register citation pairs as edges.

        Args:
            max_texts (int): Consider docs with less than N citations.
        """

        text_ids = (
            fn.array_agg(Text.id)
            .coerce(False)
            .alias('text_ids')
        )

        docs = (
            Citation
            .select(Citation.document, text_ids)
            .join(Text)
            .having(fn.count(Text.id) < text_cap)
            .where(Text.display==True)
            .where(Text.valid==True)
            .group_by(Citation.document)
        )

        for row in query_bar(docs):
            for tid1, tid2 in combinations(row.text_ids, 2):

                # If the edge exists, increment the weight.

                if self.graph.has_edge(tid1, tid2):
                    self.graph[tid1][tid2]['weight'] += 1

                # Otherwise, initialize the edge.

                else:
                    self.graph.add_edge(tid1, tid2, weight=1)


    def add_nodes(self):

        """
        Register displayed texts.
        """

        for t in progress.bar(Text_Index.rank_texts()):

            text = t['text']

            self.graph.add_node(text.id, dict(

                title   = text.pretty('title'),
                authors = text.pretty('authors'),

                count   = text.count,
                score   = t['score'],

            ))


    def trim(self):

        """
        Remove all but the largest connected component.
        """

        subgraphs = sorted(
            nx.connected_component_subgraphs(self.graph),
            key=len, reverse=True
        )

        self.graph = subgraphs[0]


    def write_gml(self, path):

        """
        Serialize the graph as .gml.

        Args:
            path (str)
        """

        nx.write_gml(self.graph, path)
