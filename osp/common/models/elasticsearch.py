

from osp.common.config import config
from elasticsearch.helpers import bulk


class ElasticsearchModel:


    @property
    def es_mapping(self):
        raise NotImplementedError


    @property
    def es_doc(self):
        raise NotImplementedError


    @property
    def es_index(self):
        raise NotImplementedError


    @property
    def es_doc_type(self):
        raise NotImplementedError


    @classmethod
    def es_query(cls):
        raise NotImplementedError


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
    def es_insert(cls):

        """
        Insert documents.
        """

        def stream():
            for row in cls.es_query():
                yield row.es_doc

        # Batch-insert the documents.
        bulk(
            config.es,
            stream(),
            raise_on_exception=False,
            doc_type=cls.es_doc_type,
            index=cls.es_index
        )

        # Commit the index.
        config.es.indices.flush(cls.es_index)


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
