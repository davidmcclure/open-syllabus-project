

from sqlalchemy import Column, String

from osp.models import BaseModel
from osp.common import config
from osp.corpus.syllabus import Syllabus
from osp.corpus.corpus import Corpus


class Document(BaseModel):


    path = Column(String, nullable=False, unique=True)


    @classmethod
    def ingest(cls):

        """
        Insert a row for each syllabus in the corpus.
        """

        corpus = Corpus.from_env()

        for syllabus in corpus.syllabi_bar():

            session = config.build_session()
            session.add(cls(path=syllabus.relative_path))

            try:
                session.commit()

            except:
                pass


    @property
    def syllabus(self):

        """
        Make a Syllabus instance.
        """

        return Syllabus.from_env(self.path)
