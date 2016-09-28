

import datetime

from bs4 import BeautifulSoup
from osp.citations.utils import tokenize_field, get_text, get_attr


class JSTOR_Record:

    def __init__(self, path):

        """
        Parse the XML.

        Args:
            path (str): The XML manifest path.
        """

        with open(path, 'rb') as fh:
            self.xml = BeautifulSoup(fh, 'lxml')

    def article_id(self):

        """
        Query the article id.

        Returns: str
        """

        return get_text(self.xml, 'article-id')

    def article_title(self):

        """
        Query the article title.

        Returns: str
        """

        return get_text(self.xml, 'article-title')

    def journal_id(self):

        """
        Query the journal id.

        Returns: str
        """

        return get_text(self.xml, 'journal-id')

    def journal_title(self):

        """
        Query the journal title.

        Returns: str
        """

        return get_text(self.xml, 'journal-title')

    def publisher_name(self):

        """
        Query the publisher name.

        Returns: str
        """

        return get_text(self.xml, 'publisher-name')

    def volume(self):

        """
        Query the volume number.

        Returns: str
        """

        return get_text(self.xml, 'volume')

    def issue(self):

        """
        Query the issue number.

        Returns: str
        """

        return get_text(self.xml, 'issue')

    def url(self):

        """
        Query the article URL.

        Returns: str
        """

        return get_attr(self.xml, 'self-uri', 'xlink:href')

    def pub_date(self):

        """
        Assemble the publication date in ISO format.

        Returns: str
        """

        try:

            date = datetime.date(
                int(get_text(self.xml, 'pub-date year')),
                int(get_text(self.xml, 'pub-date month')),
                int(get_text(self.xml, 'pub-date day')),
            )

            return date.isoformat()

        except:
            return None

    def authors(self):

        """
        Query author names.

        Returns: list
        """

        author = []
        for c in self.xml.select('contrib'):

            # Query for name parts.
            given_names = get_text(c, 'given-names')
            surname = get_text(c, 'surname')

            # Merge into single string.
            if given_names and surname:
                author.append(', '.join([surname, given_names]))

            # Accept just surname.
            elif surname:
                author.append(surname)

        return author

    def surname(self):

        """
        Get the surname of the first author.

        Returns: str
        """

        authors = self.xml.select('contrib')

        if authors:
            return get_text(authors[0], 'surname')

    def pagination(self):

        """
        Construct the page range.

        Returns: str
        """

        fpage = get_text(self.xml, 'fpage')
        lpage = get_text(self.xml, 'lpage')

        if fpage and lpage:
            return '-'.join([fpage, lpage])

        elif fpage:
            return fpage

        elif lpage:
            return lpage

        else:
            return None

    def is_queryable(self):

        """
        Does the record contain a query-able title and author?

        Returns: bool
        """

        title = self.article_title()
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
            corpus              = 'jstor',
            identifier          = self.article_id(),
            url                 = self.url(),
            title               = self.article_title(),
            surname             = self.surname(),
            authors             = self.authors(),
            publisher           = self.publisher_name(),
            date                = self.pub_date(),
            journal_title       = self.journal_title(),
            journal_identifier  = self.journal_id(),
            issue_volume        = self.volume(),
            issue_number        = self.issue(),
            pagination          = self.pagination(),
        )
