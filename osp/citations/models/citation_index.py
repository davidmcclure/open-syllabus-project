

from osp.citations.models import Citation
from osp.common.mixins.elasticsearch import Elasticsearch
from osp.common.utils import query_bar


class Citation_Index(Elasticsearch):


    es_index = 'osp'
    es_doc_type = 'citation'


    es_mapping = {
        '_id': {
            'index': 'not_analyzed',
            'store': True,
        },
        'properties': {
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

        for row in query_bar(Citation.select()):

            doc = {}

            # Local fields:

            doc['_id'] = row.id
            doc['text_id'] = row.text_id
            doc['document_id'] = row.document_id
            doc['corpus'] = row.text.corpus
            doc['min_freq'] = row.min_freq

            # Field references:

            subfield = row.subfield

            if subfield:
                doc['subfield_id'] = subfield.id
                doc['field_id'] = subfield.field_id

            # Institution reference:

            inst = row.institution

            if inst:
                doc['institution_id'] = inst.id

            yield doc
