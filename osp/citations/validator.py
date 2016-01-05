

from osp.common.utils import read_yaml


class Validator:


    def __init__(self):

        """
        Read config, initialize the citations set.
        """

        self.config = read_yaml(
            'osp.citations',
            'config/validator.yml',
        )

        self.seen = set()


    def validate(self, citation):

        """
        Validate a citation

        Args:
            citation (osp.models.Citation)

        Returns: bool
        """

        text = citation.text

        # Reject duplicates:

        if self.is_duplicate(citation):
            return False

        # Reject title == author:

        elif self.title_same_as_author(text):
            return False

        # Reject blacklisted titles.

        elif self.title_blacklisted(text):
            return False

        return True


    def is_duplicate(self, citation):

        """
        Is a citation a duplicate?

        Args:
            citation (osp.models.Citation)

        Returns: bool
        """

        pair = (citation.text.hash, citation.document_id)

        if pair in self.seen:
            return True

        else:
            self.seen.add(pair)
            return False


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
            citation (osp.models.Text)

        Returns: bool
        """

        return (
            len(text.title_tokens) == 1 and
            text.title_tokens[0] in self.config['blacklisted_titles']
        )
