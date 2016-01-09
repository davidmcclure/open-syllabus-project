

class Hit:


    def __init__(self, hit):

        """
        Set the raw Elasticsearch hit.

        Args:
            hit (dict)
        """

        self.hit = hit


    def field(self, key, delimiter=', '):

        """
        Get a document field.

        Args:
            key (str)

        Returns: str
        """

        value = self.hit['_source'][key]

        if type(value) == list:
            return delimiter.join(value)

        else:
            return value


    @property
    def count(self):

        """
        Get the citation count.

        Returns: int
        """

        return int(self.hit['sort'][0])
