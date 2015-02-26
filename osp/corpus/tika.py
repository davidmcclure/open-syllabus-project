

class Tika:


    @classmethod
    def from_env(cls):

        """
        Get an instance for the ENV-defined corpus.
        """

        return cls(config['tika']['server'])


    def __init__(self, url):

        """
        Set the URL.

        Args:
            url (str): The Tika server URL.
        """

        self.url = url
