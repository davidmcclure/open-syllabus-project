

import datetime

from bs4 import BeautifulSoup


class JSTOR_Article:


    def __init__(self, path):

        """
        Parse the XML.

        Args:
            path (str): The XML manifest path.
        """

        with open(path, 'rb') as fh:
            self.xml = BeautifulSoup(fh, 'lxml')


    def select(self, selector):

        """
        Extract text from an element.

        Args:
            selector (str)

        Returns: str
        """

        return (
            self.xml
            .select_one(selector)
            .get_text(strip=True)
            or None
        )


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
            given_names = c.select_one('given-names').get_text()
            surname = c.select_one('surname').get_text()

            # Join into a single string.
            author.append(' '.join([given_names, surname]))

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
