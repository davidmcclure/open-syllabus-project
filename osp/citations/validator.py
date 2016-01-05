

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

        pair = (text.hash, citation.document_id)

        if pair in self.seen:
            return False

        else:
            self.seen.add(pair)

        # Reject title == author:

        if text.author_tokens == text.title_tokens:
            return False

        # Reject blacklisted, single-token titles.

        if (
            len(text.title_tokens) == 1 and
            text.title_tokens[0] in self.config['blacklisted_titles']
        ):
            return False

        return True
