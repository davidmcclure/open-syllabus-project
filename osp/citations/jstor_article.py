

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


    @property
    def article_id(self):

        """
        Query the article id.

        Returns: str
        """

        return self.xml.select_one('article-id').get_text()


    @property
    def article_title(self):

        """
        Query the article title.

        Returns: str
        """

        return self.xml.select_one('article-title').get_text()


    @property
    def journal_title(self):

        """
        Query the journal title.

        Returns: str
        """

        return self.xml.select_one('journal-title').get_text()


    @property
    def publisher_name(self):

        """
        Query the publisher name.

        Returns: str
        """

        return self.xml.select_one('publisher-name').get_text()


    @property
    def volume(self):

        """
        Query the volume number.

        Returns: str
        """

        return self.xml.select_one('volume').get_text()


    @property
    def issue(self):

        """
        Query the issue number.

        Returns: str
        """

        return self.xml.select_one('issue').get_text()


    @property
    def pub_date(self):

        """
        Assemble the publication date in ISO format.

        Returns: str
        """

        date = datetime.date(
            int(self.xml.select_one('pub-date year').get_text()),
            int(self.xml.select_one('pub-date month').get_text()),
            int(self.xml.select_one('pub-date day').get_text()),
        )

        return date.isoformat()


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

        fpage = self.xml.select_one('fpage').get_text()
        lpage = self.xml.select_one('lpage').get_text()

        if fpage and lpage:
            return '-'.join([fpage, lpage])

        elif fpage:
            return fpage

        elif lpage:
            return lpage

        else:
            return None
