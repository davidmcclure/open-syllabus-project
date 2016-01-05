

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

        pass
