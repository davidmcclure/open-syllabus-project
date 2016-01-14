

import inflect
import iso3166
import us

from cached_property import cached_property

from osp.common import config
from osp.common.utils import read_yaml
from osp.constants import redis_keys



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

        self.max_fuzz = max_fuzz

        self.config = Config()


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

        # Reject toponyms in title/author.

        elif self.has_toponym(text):
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

        # Check for an existing hash -> id.

        tid = config.redis.hget(
            redis_keys.OSP_DEDUP,
            text.hash,
        )

        if tid is None:

            # Lock hash -> id, if the hash is new.

            config.redis.hset(
                redis_keys.OSP_DEDUP,
                text.hash, text.id,
            )

            return False

        else:
            return int(tid) != text.id


    def title_same_as_author(self, text):

        """
        Is a text's title the same as the author?

        Args:
            citation (osp.models.Text)

        Returns: bool
        """

        return text.surname_tokens == text.title_tokens


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


    def has_toponym(self, text):

        """
        Does the text's title or author consist of a US state or country?

        Args:
            text (osp.models.Text)

        Returns: bool
        """

        a = ' '.join(text.surname_tokens)
        t = ' '.join(text.title_tokens)

        return (

            # US states
            us.states.lookup(a) or
            us.states.lookup(t) or

            # Countries
            iso3166.countries.get(a, None) or
            iso3166.countries.get(t, None)

        )


    def fuzzy_tokens(self, citation):

        """
        Are the query tokens sufficiently focused?

        Args:
            citation (osp.models.Citation)

        Returns: bool
        """

        return citation.fuzz > self.max_fuzz
