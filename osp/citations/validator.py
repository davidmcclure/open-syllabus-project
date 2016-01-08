

import inflect

from cached_property import cached_property

from osp.common.utils import read_yaml


class Config:


    def __init__(self,
        package='osp.citations',
        path='config/validator.yml',
    ):

        """
        Parse the config file.
        """

        self.config = read_yaml(package, path)


    @cached_property
    def blacklisted_titles(self):

        """
        Provide a list of blacklisted title tokens, with plurals.

        Returns: list
        """

        p = inflect.engine()

        singulars = self.config['blacklisted_titles']

        return singulars + [p.plural(s) for s in singulars ]


class Validator:


    def __init__(self, max_fuzz=float('inf')):

        """
        Read config, initialize the citations set.

        Args:
            max_fuzz (int): The maximum allowable fuzz score.
        """

        self.config = Config()

        self.max_fuzz = max_fuzz

        self.seen = {}


    def validate(self, citation):

        """
        Validate a citation

        Args:
            citation (osp.models.Citation)

        Returns: bool
        """

        text = citation.text

        # Reject duplicates:

        if self.is_duplicate(text):
            return False

        # Reject title == author:

        elif self.title_same_as_author(text):
            return False

        # Reject blacklisted titles.

        elif self.title_blacklisted(text):
            return False

        # Reject unfocused tokens.

        elif self.fuzzy_tokens(citation):
            return False

        return True


    def is_duplicate(self, text):

        """
        Is a text a duplicate?

        Args:
            citation (osp.models.Citation)

        Returns: bool
        """

        tid = self.seen.get(text.hash)

        if tid is None:
            self.seen[text.hash] = text.id
            return False

        else:
            return tid != text.id


    def title_same_as_author(self, text):

        """
        Is a text's title the same as the author?

        Args:
            citation (osp.models.Text)

        Returns: bool
        """

        return text.author_tokens == text.title_tokens


    def title_blacklisted(self, text):

        """
        Is a text's title a single blacklisted token?

        Args:
            text (osp.models.Text)

        Returns: bool
        """

        return (
            len(text.title_tokens) == 1 and
            text.title_tokens[0] in self.config.blacklisted_titles
        )


    def fuzzy_tokens(self, citation):

        """
        Are the query tokens sufficiently focused?

        Args:
            citation (osp.models.Citation)

        Returns: bool
        """

        return citation.fuzz > self.max_fuzz
