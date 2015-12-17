

import random

from osp.common.mixins.elasticsearch import Elasticsearch

from clint.textui import progress


class Citation_Index(Elasticsearch):


    es_index = 'osp'
    es_doc_type = 'citation'


    es_mapping = {
        '_id': {
            'path': 'citation_id',
        },
        'properties': {
            'citation_id': {
                'type': 'integer'
            },
            'text_id': {
                'type': 'integer'
            },
            'document_id': {
                'type': 'integer'
            },
            'corpus': {
                'type': 'string'
            },
            'min_freq': {
                'type': 'float'
            },
            'subfield_id': {
                'type': 'integer'
            },
            'field_id': {
                'type': 'integer'
            },
            'institution_id': {
                'type': 'integer'
            },
        }
    }


    @classmethod
    def es_stream_docs(cls):

        """
        Stream Elasticsearch docs.

        Yields:
            dict: The next document.
        """

        for i in progress.bar(range(1000000)):

            yield dict(
                citation_id     = i,
                text_id         = random.randint(1, 200000),
                document_id     = random.randint(1, 1500000),
                corpus          = random.choice(['hlom', 'jstor']),
                min_freq        = random.uniform(0, 10),
                institution_id  = random.randint(0, 1000),
                field_id        = random.randint(0, 10),
                subfield_id     = random.randint(0, 200),
            )
