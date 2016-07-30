

from multiprocessing import Pool
from playhouse.postgres_ext import ServerSide

from osp.institutions.utils import seed_to_regex
from osp.institutions.models import Institution, Institution_Document
from osp.corpus.models import Document


class DocToInst:

    @classmethod
    def run(cls):

        """
        Create the pool, map docs.
        """

        docs = Document.select()

        with Pool() as pool:
            pool.map(cls(), docs)

    def __init__(self):

        """
        Initialize the regex -> institution map.
        """

        self.regex_inst = [
            (seed_to_regex(inst.url), inst)
            for inst in ServerSide(Institution.select())
            if inst.url
        ]

    def __call__(self, doc):

        """
        Match a document URL to an institution, write a link row.

        Args:
            doc(Document)
        """

        try:

            url = doc.syllabus.url

            # Probe for a matching institution.
            for regex, inst in self.regex_inst:
                if regex.search(url):

                    # Write the link row.
                    Institution_Document.create(
                        document=doc,
                        institution=inst,
                    )

        except Exception as e:
            print(e)
