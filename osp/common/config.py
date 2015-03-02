

import os
import anyconfig


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

        self.config = anyconfig.load(
            paths,
            merge=anyconfig.MS_DICTS,
            ignore_missing=True
        )


    def __getitem__(self, key):

        """
        Get a configuration value.

        Args:
            key (str): The configuration key.

        Returns:
            The option value.
        """

        return self.config[key]


# Global instance.
config = Config.from_env()
