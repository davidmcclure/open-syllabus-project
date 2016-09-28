

from osp.citations.utils import clean_field, tokenize_field


class HLOM_Record:

    def __init__(self, record):

        """
        Set the MARC record.

        Args:
            record (pymarc.Record): The raw MARC record.
        """

        self.record = record

    def control_number(self):

        """
        Get the control number.

        Returns: str
        """

        return clean_field(self.record['001'].format_field())

    def title(self):

        """
        Get the title.

        Returns: str
        """

        return clean_field(self.record.title())

    def authors(self):

        """
        Get the author array.

        Returns: list
        """

        author = clean_field(self.record.author())
        return [author] if author else []

    def surname(self):

        """
        Extract a surname.

        Returns: surname
        """

        author = clean_field(self.record.author())
        return author.split(',')[0] if author else None

    def publisher(self):

        """
        Get the publisher.

        Returns: str
        """

        return clean_field(self.record.publisher())

    def date(self):

        """
        Get the date.

        Returns: str
        """

        return clean_field(self.record.pubyear())

    def is_queryable(self):

        """
        Does the record contain a query-able title and author?

        Returns: bool
        """

        title = self.title()
        surname = self.surname()

        return bool(
            title and
            len(tokenize_field(title)) and
            surname and
            len(tokenize_field(surname))
        )

    def text(self):

        """
        Assemble text fields.

        Returns: dict
        """

        return dict(
            corpus      = 'hlom',
            identifier  = self.control_number(),
            title       = self.title(),
            surname     = self.surname(),
            authors     = self.authors(),
            publisher   = self.publisher(),
            date        = self.date(),
        )
