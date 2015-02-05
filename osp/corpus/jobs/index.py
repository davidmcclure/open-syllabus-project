

from osp.corpus.queries import all_document_texts
from osp.common.models.base import elasticsearch as es
from elasticsearch.helpers import bulk


def index(page_number, records_per_page):

    """
    Index a page of OSP records.

    :param page_number: The 1-indexed page number.
    :param records_per_page: Records in the page.
    """

    page = (
        all_document_texts()
        .paginate(page_number, records_per_page)
    )

    docs = []
    for doc in page.iterator():
        docs.append({
            '_id': doc.document,
            'body': doc.text
        })

    # Bulk-index the page.
    bulk(es, docs, index='osp', doc_type='syllabus')
