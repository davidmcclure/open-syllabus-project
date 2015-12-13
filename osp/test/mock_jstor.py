

import os
import pkgutil
import datetime
import uuid

from jinja2 import Template
from osp.test.mock_corpus import Mock_Corpus


class Mock_JSTOR(Mock_Corpus):


    def __init__(self):

        """
        Compile the XML template.
        """

        super().__init__()

        tpl = pkgutil.get_data('osp.test', 'templates/jstor.j2')
        self.template = Template(tpl.decode('utf8'))


    def add_article(self,

        journal_slug='journal',
        article_id=None,

        journal_title='Journal',
        publisher_name='Publisher',
        article_title='Article',

        pub_year=1987,
        pub_month=6,
        pub_day=25,

        author=[('David W.', 'McClure'),],

    ):

        """
        Add an XML record to the corpus.

        Returns:
            str: The path of the new file.
        """

        # Generate an article id.
        if not article_id:
            article_id = str(uuid.uuid4())

        args = locals().copy()
        args.pop('self')

        # Template the XML.
        xml = self.template.render(args)

        # Form the publication date.
        date = datetime.date(pub_year, pub_month, pub_day)

        rel_path = '/'.join([
            journal_slug,
            date.isoformat(),
            article_id,
            article_id+'.xml',
        ])

        path = os.path.join(self.path, rel_path)

        # Ensure the directory.
        os.makedirs(os.path.dirname(path))

        with open(path, 'w') as fh:
            print(xml, file=fh)

        return path
