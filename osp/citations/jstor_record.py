

import datetime

from bs4 import BeautifulSoup
from osp.citations.utils import tokenize_field


class JSTOR_Record:


    def __init__(self, path):

        """
        Parse the XML.

        Args:
            path (str): The XML manifest path.
        """

        with open(path, 'rb') as fh:
            self.xml = BeautifulSoup(fh, 'lxml')


    def select(self, selector, root=None):

        """
        Extract text from an element.

        Args:
            selector (str)

        Returns: str
        """

        root = root or self.xml

        tag = root.select_one(selector)

        if tag:
            return tag.get_text(strip=True) or None

        else:
            return None


    @property
    def article_id(self):

        """
        Query the article id.

        Returns: str
        """

        return self.select('article-id')


    @property
    def article_title(self):

        """
        Query the article title.

        Returns: str
        """

        return self.select('article-title')


    @property
    def journal_id(self):

        """
        Query the journal id.

        Returns: str
        """

        return self.select('journal-id')


    @property
    def journal_title(self):

        """
        Query the journal title.

        Returns: str
        """

        return self.select('journal-title')


    @property
    def publisher_name(self):

        """
        Query the publisher name.

        Returns: str
        """

        return self.select('publisher-name')


    @property
    def volume(self):

        """
        Query the volume number.

        Returns: str
        """

        return self.select('volume')


    @property
    def issue(self):

        """
        Query the issue number.

        Returns: str
        """

        return self.select('issue')


    @property
    def pub_date(self):

        """
        Assemble the publication date in ISO format.

        Returns: str
        """

        try:

            date = datetime.date(
                int(self.select('pub-date year')),
                int(self.select('pub-date month')),
                int(self.select('pub-date day')),
            )

            return date.isoformat()

        except:
            return None


    @property
    def author(self):

        """
        Query author names.

        Returns: list
        """

        author = []
        for c in self.xml.select('contrib'):

            # Query for name parts.
            given_names = self.select('given-names', c)
            surname = self.select('surname', c)

            # Merge into single string.
            if given_names and surname:
                author.append(' '.join([given_names, surname]))

            # Accept just surname.
            elif surname:
                author.append(surname)

        return author


    @property
    def pagination(self):

        """
        Construct the page range.

        Returns: str
        """

        fpage = self.select('fpage')
        lpage = self.select('lpage')

        if fpage and lpage:
            return '-'.join([fpage, lpage])

        elif fpage:
            return fpage

        elif lpage:
            return lpage

        else:
            return None


    @property
    def is_queryable(self):

        """
        Does the record contain a query-able title and author?

        Returns: bool
        """

        title = self.article_title
        author = self.author

        return bool(
            title and
            len(tokenize_field(title)) and
            len(author) and
            len(tokenize_field(author[0]))
        )
