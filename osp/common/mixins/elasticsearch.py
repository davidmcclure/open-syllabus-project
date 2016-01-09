

from osp.common import config
from elasticsearch.client import _make_path
from elasticsearch.helpers import bulk


class Elasticsearch:


    @property
    def es_mapping(self):
        raise NotImplementedError


    @classmethod
    def es_stream_docs(cls):
        raise NotImplementedError


    @classmethod
    def es_stream_mock_docs(cls):
        raise NotImplementedError


    @property
    def es_index(self):
        raise NotImplementedError


    @classmethod
    def es_create(cls):

        """
        Set the mapping.
        """

        # Ensure the index.
        try: config.es.indices.create(cls.es_index)
        except: pass

        # Create the mapping.
        config.es.indices.put_mapping(
            index=cls.es_index,
            doc_type=cls.es_index,
            body=cls.es_mapping,
        )


    @classmethod
    def es_delete(cls):

        """
        Delete the mapping.
        """

        try: config.es.indices.delete(cls.es_index)
        except: pass


    @classmethod
    def es_insert(cls, mock=False):

        """
        Insert documents.

        Args:
            mock (bool): If true, generate mock data.
        """

        if not mock:
            actions = cls.es_stream_docs()

        else:
            actions = cls.es_stream_mock_docs()

        # Clear the index.
        cls.es_reset()

        # Batch-insert the documents.
        bulk(
            client=config.es,
            actions=actions,
            raise_on_exception=False,
            raise_on_error=False,
            doc_type=cls.es_index,
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

        r = config.es.count(
            index=cls.es_index,
            doc_type=cls.es_index,
        )

        return r['count']


    @classmethod
    def es_reset(cls):

        """
        Clear and recreate the index.
        """

        cls.es_delete()
        cls.es_create()
