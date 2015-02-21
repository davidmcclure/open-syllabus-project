

import hashlib
import spacy.en
import re

from osp.common.models.base import LocalModel
from osp.citations.hlom.utils import sanitize_query, clean_field
from peewee import *
from playhouse.postgres_ext import *
from pymarc import Record


# Load spaCy.
nlp = spacy.en.English()


class HLOM_Record(LocalModel):


    control_number = CharField(unique=True)
    metadata = HStoreField()
    stored_id = BigIntegerField(null=True)
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

        # Downcase, tokenize.
        query = self.query.lower()
        tokens = nlp(query)

        # Remove articles, punct, and whitespace.
        filtered = [t.orth_ for t in tokens if
                    t.pos_ not in ['DET', 'PUNCT'] and
                    not re.match('^\s+$', t.orth_)]

        # Get an sha1 digest.
        sha1 = hashlib.sha1()
        sha1.update(''.join(filtered).encode('ascii', 'ignore'))
        return sha1.hexdigest()


    @property
    def document(self):

        """
        Construct an Elasticsearch document.
        """

        # Get raw subject / notes values.
        subjs = [s.format_field() for s in self.pymarc.subjects()]
        notes = [n.format_field() for n in self.pymarc.notes()]

        return {
            '_id':          self.control_number,
            'author':       clean_field(self.pymarc.author()),
            'title':        clean_field(self.pymarc.title()),
            'pubyear':      self.pymarc.pubyear(),
            'publisher':    self.pymarc.publisher(),
            'subjects':     subjs,
            'notes':        notes,
            'count':        int(self.metadata['citation_count']),
            'rank':         int(self.metadata['teaching_rank']),
            'percentile':   float(self.metadata['teaching_percentile']),
            'stored_id':    self.stored_id
        }
