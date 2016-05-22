

from sqlalchemy import Column, String

from osp.models import BaseModel


class Document(BaseModel):

    path = Column(String, nullable=False)
