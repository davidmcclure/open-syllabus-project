

from osp.common.utils import query_bar
from osp.citations.models import Text, Citation
from osp.corpus.models import Document

import networkx as nx
from peewee import fn


class Text_Graph:


    def __init__(self):

        """
        Initialize the graph instance.
        """

        self.graph = nx.Graph()


    def add_edges(self):

        """
        For each syllabus, register citation pairs as edges.
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
            .where(Text.display==True)
            .where(Text.valid==True)
            .group_by(Citation.document)
        )

        for row in query_bar(docs):
            print(row.text_ids)


    def hydrate_nodes(self):

        """
        Load text metadata onto the nodes.
        """

        pass
