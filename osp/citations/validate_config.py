

import inflect

from osp.citations.utils import tokenize_field
from osp.common.utils import read_yaml


class Validate_Config:


    def __init__(self, package='osp.citations', path='config/validate.yml'):

        """
        Read the config file.
        """

        self.config = read_yaml(package, path)


    @property
    def max_fuzz(self):

        """
        Get the max fuzz value.

        Returns: float
        """

        return self.config.get('max_fuzz', float('inf'))


    @property
    def blacklisted_titles(self):

        """
        Pluralize the blacklisted titles.

        Returns: list
        """

        p = inflect.engine()

        singulars = self.config.get('blacklisted_titles', [])

        return map(
            tokenize_field,
            singulars + [p.plural(s) for s in singulars],
        )


    @property
    def blacklisted_surnames(self):

        """
        Pluralize the blacklisted surnames.

        Returns: list
        """

        return map(
            tokenize_field,
            self.config.get('blacklisted_surnames', [])
        )


    @property
    def whitelist(self):

        """
        Get the set of whitelisted ids.

        Returns: list
        """

        return self.config.get('whitelist', [])
