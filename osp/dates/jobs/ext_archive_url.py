

import re

from osp.corpus.models.document import Document
from osp.dates.models.archive_url import Document_Date_Archive_Url
from datetime import datetime


date_format = '%Y%m%d%H%M%S'


def ext_archive_url(id):

    """
    Try to extract an Internet Archive timestamp from the URL.

    Args:
        id (int): The document id.
    """

    doc = Document.get(Document.id==id)

    match = re.search(
        'web\.archive\.org\/web\/(?P<timestamp>\d+)',
        doc.syllabus.url
    )

    if match:

        date = datetime.strptime(
            match.group('timestamp'),
            date_format
        )

        if date < datetime.now():

            Document_Date_Archive_Url.create(
                document=doc,
                date=date
            )
