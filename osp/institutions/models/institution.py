

from osp.common.config import config
from osp.common.mixins.elasticsearch import Elasticsearch
from osp.common.models.base import BaseModel
from osp.common.utils import read_csv
from playhouse.postgres_ext import BinaryJSONField


class Institution(BaseModel, Elasticsearch):


    metadata = BinaryJSONField(default={})


    class Meta:
        database = config.get_table_db('institution')


    es_index = 'osp'
    es_doc_type = 'institution'


    es_mapping = {
        '_id': {
            'index': 'not_analyzed',
            'store': True
        },
        'properties': {
            'name': {
                'type': 'string'
            },
            'city': {
                'type': 'string'
            },
            'state': {
                'type': 'string'
            }
        }
    }


    @classmethod
    def es_stream_docs(cls):

        """
        Index institutions with cited syllabi.

        Yields:
            dict: The next document.
        """

        # TODO: De-circularize.
        from osp.locations.models.doc_inst import Document_Institution
        from osp.citations.hlom.models.citation import HLOM_Citation

        cited = (

            cls.select()
            .group_by(cls.id)

            # Join citations.
            .join(Document_Institution)
            .join(HLOM_Citation, on=(
                Document_Institution.document==HLOM_Citation.document
            ))

        )

        for inst in cited:

            name = (
                inst.metadata['Campus_Name'] or
                inst.metadata['Institution_Name']
            )

            city = (
                inst.metadata['Campus_City'] or
                inst.metadata['Institution_City']
            )

            state = inst.metadata['Institution_State']

            yield {
                '_id': inst.id,
                'name': name,
                'state': state,
                'city': city
            }


    @classmethod
    def insert_institutions(cls):

        """
        Write institution rows into the database.
        """

        reader = read_csv(
            'osp.institutions',
            'data/institutions.csv'
        )

        rows = []
        for row in reader:
            rows.append({'metadata': row})

        with cls._meta.database.transaction():
            cls.insert_many(rows).execute()


    @property
    def geocoding_query(self):

        """
        Build a geolocation query.
        """

        # Campus address:
        c_street = self.metadata['Campus_Address']
        c_city   = self.metadata['Campus_City']
        c_state  = self.metadata['Campus_State']

        if c_street and c_city and c_state:
            return ','.join([c_street, c_city, c_state, 'USA'])

        # Or, institution address:
        i_street = self.metadata['Institution_Address']
        i_city   = self.metadata['Institution_City']
        i_state  = self.metadata['Institution_State']

        if i_street and i_city and i_state:
            return ','.join([i_street, i_city, i_state, 'USA'])
