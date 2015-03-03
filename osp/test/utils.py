

from osp.common.config import config
from playhouse.test_utils import test_database
from contextlib import contextmanager


@contextmanager
def db(*models):

    """
    Assign the passed models to the testing database.

    Args:
        models (*peewee.Model): The models under test.

    Yields:
        A context with the wrapped models.
    """

    with test_database(config.get_db('test'), list(models)):
        yield
