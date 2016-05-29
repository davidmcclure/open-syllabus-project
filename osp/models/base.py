

import inflection

from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, Integer


class _BaseModel:


    @declared_attr
    def __tablename__(cls):

        """
        Use the snake-cased class name as the table name.

        Returns: str
        """

        # TODO: "_" prefix during migration.

        return '_'+inflection.underscore(cls.__name__)


    id = Column(Integer, primary_key=True)


BaseModel = declarative_base(cls=_BaseModel)
