

import re

from osp.citations.hlom.models.record import HLOM_Record
from osp.common.models.base import elasticsearch as es
from pymarc.record import Record
from elasticsearch.helpers import bulk


def index(page_number, records_per_page):

    """
    Index a page of HLOM records.

    :param page_number: The 1-indexed page number.
    :param records_per_page: Records in the page.
    """

    page = (
        HLOM_Record
        .select()
        .paginate(page_number, records_per_page)
        .order_by(HLOM_Record.id)
    )

    docs = []
    for row in page.iterator():

        # Hydrate a MARC record.
        marc = row.pymarc_record()

        # Get raw subject/notes values.
        subjects = [s.format_field() for s in marc.subjects()]
        notes = [n.format_field() for n in marc.notes()]

        docs.append({
            '_id': row.control_number,
            'title': marc.title(),
            'author': marc.author(),
            'publisher': marc.publisher(),
            'pubyear': marc.pubyear(),
            'subjects': subjects,
            'notes': notes
        })

    # Bulk-index the page.
    bulk(es, docs, index='hlom', doc_type='record')
