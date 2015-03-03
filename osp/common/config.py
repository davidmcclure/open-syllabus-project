

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
        Get a Postgres database object for a given table name.

        Args:
            table (str): The name of the table.

        Returns:
            PostgresqlExtDatabase: The database object.
        """

        defaults = self['postgres']['default']['params']

        # Try to find a custom host.
        params = None
        for name, host in self['postgres'].items():
            if table in host.get('tables', []):

                # Merge the custom params with the defaults.
                params = dict(
                    list(defaults.items()) +
                    list(host['params'].items())
                )

        # If none is found, use the defaults.
        if not params:
            params = defaults

        return PostgresqlExtDatabase(**params)


# Global instance.
config = Config.from_env()
