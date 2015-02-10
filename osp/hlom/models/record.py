

import spacy.en
import re

from osp.common.models.base import LocalModel
from osp.citations.hlom.utils import sanitize_query
from peewee import *
from playhouse.postgres_ext import *
from pymarc import Record


# Load spaCy.
nlp = spacy.en.English()


class HLOM_Record(LocalModel):


    control_number = CharField(unique=True)
    record = BlobField()


    @property
    def pymarc(self):

        """
        Wrap the raw record blob as a Pymarc record instance.
        """

        return Record(
            data=bytes(self.record),
            ascii_handling='ignore',
            utf8_handling='ignore'
        )


    @property
    def query(self):

        """
        Build an Elasticsearch query string.
        """

        return sanitize_query(' '.join([
            self.pymarc.title(),
            self.pymarc.author()
        ]))


    @property
    def hash(self):

        """
        Generate a "grouping" hash, for de-duplication.
        """

        # Downcase the query.
        query = self.query.lower()

        # Tokenize / tag.
        tokens = nlp(query)

        # Remove articles, punct, and whitespace.
        filtered = [t.orth_ for t in tokens if
                    t.pos_ not in ['DET', 'PUNCT'] and
                    not re.match('^\s+$', t.orth_)]

        return ''.join(filtered)
