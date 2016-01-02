

from osp.citations.utils import clean_field, tokenize_field


class HLOM_Record:


    def __init__(self, record):

        """
        Set the MARC record.

        Args:
            record (pymarc.Record): The raw MARC record.
        """

        self.record = record


    @property
    def control_number(self):

        """
        Get the control number.

        Returns: str
        """

        return clean_field(self.record['001'].format_field())


    @property
    def title(self):

        """
        Get the title.

        Returns: str
        """

        return clean_field(self.record.title())


    @property
    def authors(self):

        """
        Get the author array.

        Returns: list
        """

        author = clean_field(self.record.author())
        return [author] if author else []


    @property
    def surname(self):

        """
        Extract a surname.

        Returns: surname
        """

        author = clean_field(self.record.author())
        return author.split(',')[0] if author else None


    @property
    def publisher(self):

        """
        Get the publisher.

        Returns: str
        """

        return clean_field(self.record.publisher())


    @property
    def date(self):

        """
        Get the date.

        Returns: str
        """

        return clean_field(self.record.pubyear())


    @property
    def is_queryable(self):

        """
        Does the record contain a query-able title and author?

        Returns: bool
        """

        title = self.title
        authors = self.authors

        return bool(
            title and
            len(tokenize_field(title)) and
            len(authors) and
            len(tokenize_field(authors[0]))
        )
