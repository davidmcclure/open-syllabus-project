

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


    def trim(self):

        """
        Remove all but the largest connected component.
        """

        subgraphs = sorted(
            nx.connected_component_subgraphs(self.graph),
            key=len, reverse=True
        )

        self.graph = subgraphs[0]


    def write_graphml(self, path):

        """
        Serialize the graph as .graphml.

        Args:
            path (str)
        """

        nx.write_graphml(self.graph, path)
