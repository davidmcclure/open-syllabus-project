

import networkx as nx

from osp.common.utils import query_bar
from osp.graphs.graph import Graph
from osp.citations.models import Text, Citation, Text_Index
from osp.corpus.models import Document

from itertools import combinations
from peewee import fn
from clint.textui import progress


class OSP_Graph(Graph):


    def add_edges(self, max_texts=20):

        """
        For each syllabus, register citation pairs as edges.

        Args:
            max_texts (int): Ignore docs with > than N citations.
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
            .having(fn.count(Text.id) <= max_texts)
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
                author  = text.pretty('authors')[0],
                label   = text.pretty('title'),

                count   = text.count,
                score   = t['score'],

            ))


    def trim_unconnected_components(self):

        """
        Remove all but the largest connected component.
        """

        subgraphs = sorted(
            nx.connected_component_subgraphs(self.graph),
            key=len, reverse=True
        )

        self.graph = subgraphs[0]


    def trim_texts_by_count(self, min_count=100):

        """
        Remove all texts with counts below a threshold.

        Args:
            min_count (int)
        """

        for tid, text in self.graph.nodes(data=True):
            if text['count'] < min_count:
                self.graph.remove_node(tid)


    def trim_edges(self, keep=0.5):

        """
        Randomly prune a certain percentage of edges.

        Args:
            keey (float)
        """

        for tid1, tid2 in self.graph.edges():
            if random.random() > keep:
                self.graph.remove_edge(tid1, tid2)
