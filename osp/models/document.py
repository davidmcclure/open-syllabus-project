

from sqlalchemy import Column, String

from osp.common import config
from osp.models import BaseModel


class Document(BaseModel):


    path = Column(String, nullable=False, index=True)


    @classmethod
    def insert_documents(cls):

        """
        Load a row for each syllabus in the corpus.
        """

        corpus = Corpus.from_env()

        with config.transaction() as session:

            for syllabus in corpus.syllabi_bar():
                session.add(cls(path=syllabus.relative_path))
