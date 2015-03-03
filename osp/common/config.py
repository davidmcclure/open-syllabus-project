

import os
import anyconfig

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

            # Defaults first.
            os.path.join(os.path.dirname(__file__), 'osp.yml'),

            # Custom configs.
            '/etc/osp/osp.yml',
            '~/osp.yml',
            './osp.yml'

        ])


    def __init__(self, paths):

        """
        Initialize the configuration object.

        Args:
            paths (list): YAML paths, from the most to least specific.
        """

        self.config = anyconfig.load(paths, ignore_missing=True)


    def __getitem__(self, key):

        """
        Get a configuration value.

        Args:
            key (str): The configuration key.

        Returns:
            The option value.
        """

        return self.config[key]


    def get_db(self, table):

        """
        Get a Postgres database object for a table name.

        Args:
            table (str): The name of the table.

        Returns:
            The database object.
        """

        defaults = self['postgres']['default']['args']

        # Try to find a custom host.
        args = None
        for db in self['postgres'].values():
            if table in db.get('tables', {}):

                # Merge in the default args.
                args = dict(
                    list(defaults.items()) +
                    list(db['args'].items())
                )

        # If none is found, use defaults.
        if not args:
            args = defaults

        return PostgresqlExtDatabase(**args)


# Global instance.
config = Config.from_env()
