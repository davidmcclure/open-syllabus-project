

import us

from iso3166 import countries
from clint.textui import progress
from peewee import fn

from osp.common import config
from osp.common.mixins.elasticsearch import Elasticsearch
from osp.common.utils import query_bar



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
            'count': {
                'type': 'integer'
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

        # TODO: fix
        from osp.institutions.models import Institution
        from osp.institutions.models import Institution_Document
        from osp.citations.models import Citation

        count = fn.count(Citation.id)

        query = (
            Institution
            .select(Institution, count)
            .join(Institution_Document)
            .join(Citation, on=(
                Citation.document==Institution_Document.document
            ))
            .group_by(Institution)
        )

        for row in query_bar(query):

            yield dict(
                _id = row.id,
                name = row.name,
                count = row.count,
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
