

from pymarc import Record

from osp.citations.hlom.utils import sanitize_query


class MARC(Record):


    def es_query(self):

        """
        Construct a query for Elasticsearch.

        Returns:
            str|None: The query, or None if the record fails validation.
        """

        return sanitize_query(' '.join([
            self.marc.title(),
            self.marc.author()
        ]))
