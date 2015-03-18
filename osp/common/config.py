

import os
import anyconfig
import copy

from playhouse.postgres_ext import PostgresqlExtDatabase


# Throttle the logging.
anyconfig.set_loglevel('WARNING')


class Config:


    @classmethod
    def from_env(cls):

        """
        Get a config instance with the default file precedence.
        """

        return cls([
            os.path.join(os.path.dirname(__file__), 'osp.yml'),
            '/etc/osp/osp.yml',
        ])


    def __init__(self, paths):

        """
        Initialize the configuration object.

        Args:
            paths (list): YAML paths, from the most to least specific.
        """

        self.config = anyconfig.load(paths, ignore_missing=True)

        # Save a copy of the original values.
        self.initial = copy.deepcopy(self.config.copy())


    def __getitem__(self, key):

        """
        Get a configuration value.

        Args:
            key (str): The configuration key.

        Returns:
            The option value.
        """

        return self.config[key]


    def reset(self):

        """
        Restore the initial options.
        """

        self.config.update(self.initial)


    def get_db(self, name):

        """
        Get a Postgres database object.

        Args:
            name (str): The database key.

        Returns:
            The database object.
        """

        defaults = self['postgres']['default']['args']

        db = (
            self['postgres']
            .get(name, {})
            .get('args', {})
        )

        args = dict(
            list(defaults.items()) +
            list(db.items())
        )

        return PostgresqlExtDatabase(autorollback=True, **args)


    def get_table_db(self, table):

        """
        Get a Postgres database object for a table name.

        Args:
            table (str): The name of the table.

        Returns:
            The database object.
        """

        name = None

        # Try to find a custom host.
        for key, db in self['postgres'].items():
            if table in db.get('tables', {}):
                name = key

        return self.get_db(name)


# Global instance.
config = Config.from_env()
