

import us

from osp.common.config import config
from osp.common.utils import query_bar
from osp.common.mixins.elasticsearch import Elasticsearch
from osp.institutions.models import Institution

from iso3166 import countries
from clint.textui import progress


class Institution_Index(Elasticsearch):


    es_index = 'institution'


    es_mapping = {
        '_id': {
            'index': 'not_analyzed',
            'store': True,
        },
        'properties': {
            'name': {
                'type': 'string'
            },
        }
    }


    @classmethod
    def es_stream_docs(cls):

        """
        Index institutions.

        Yields:
            dict: The next document.
        """

        for row in query_bar(Institution.select()):

            yield dict(
                _id = row.id,
                name = row.name,
            )


    @classmethod
    def materialize_institution_facets(cls, counts):

        """
        Materialize institution facet counts.

        Returns:
            dict: {label, value, count}
        """

        ids = [c[0] for c in counts]

        result = config.es.mget(
            index = cls.es_index,
            doc_type = cls.es_index,
            body = { 'ids': ids }
        )

        facets = []
        for i, doc in enumerate(result['docs']):

            facets.append(dict(
                label = doc['_source']['name'],
                value = int(doc['_id']),
                count = counts[i][1]
            ))

        return facets


    @classmethod
    def materialize_state_facets(cls, counts):

        """
        Materialize state facet counts.

        Returns:
            dict: {label, value, count}
        """

        facets = []
        for abbr, count in counts:

            state = us.states.lookup(abbr)

            if state:
                facets.append(dict(
                    label = state.name,
                    value = abbr.upper(),
                    count = count,
                ))

        return facets


    @classmethod
    def materialize_country_facets(cls, counts):

        """
        Materialize country facet counts.

        Returns:
            dict: {label, value, count}
        """

        facets = []
        for abbr, count in counts:

            country = countries.get(abbr)

            if country:
                facets.append(dict(
                    label = country.name,
                    value = abbr.upper(),
                    count = count,
                ))

        return facets
