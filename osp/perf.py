

import random
import requests
import re

from osp.common.mixins.elasticsearch import Elasticsearch

from clint.textui import progress


class Faker:


    def __init__(self, text_url='http://goo.gl/OJR4J0'):

        """
        Load and clean a text URL.

        Args:
            text_url (str)
        """

        r = requests.get(text_url)
        self.text = re.sub('\s{2,}', ' ', r.text).strip()


    def snippet(self, length):

        """
        Get a random text snippet.

        Args:
            length (int)
        """

        start = random.randrange(0, len(self.text)-length)
        return self.text[start:start+length]


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


class Text_Index(Elasticsearch):


    es_index = 'osp'
    es_doc_type = 'text'


    es_mapping = {
        '_id': {
            'path': 'text_id',
        },
        'properties': {
            'text_id': {
                'type': 'integer'
            },
            'title': {
                'type': 'string'
            },
            'author': {
                'type': 'string'
            },
            'publisher': {
                'type': 'string'
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

        faker = Faker()

        for i in progress.bar(range(200000)):

            yield dict(
                text_id     = i,
                title       = faker.snippet(100),
                author      = faker.snippet(40),
                publisher   = faker.snippet(60),
            )
