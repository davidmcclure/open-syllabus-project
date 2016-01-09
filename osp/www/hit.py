

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


    @property
    def path(self):

        """
        Get the URL path.

        Returns: str
        """

        return '/text/{0}/{1}'.format(
            self.field('corpus'),
            self.field('identifier'),
        )
