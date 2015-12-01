

from osp.fields.models.field import Field


def query(id):

    """
    Find syllabi that belong to a field.

    :param id: The field id.
    """

    field = Field.get(Field.id==id)

    for pattern in field.query_regexes('{:s}\s+[0-9]{{2,4}}'):
        pass
