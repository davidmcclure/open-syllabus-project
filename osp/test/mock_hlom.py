

import os
import tempfile
import shutil
import uuid

from contextlib import contextmanager
from pymarc import Record, Field, MARCWriter

from osp.citations.models import Text
from osp.test.mock_corpus import Mock_Corpus


class Mock_MARC(Record):

    def control_number(self):

        """
        Get 001.

        Returns:
            str: The control number.
        """

        return self['001'].format_field()

    def set_control_number(self, control_number):

        """
        Set 001.

        Args:
            control_number (str): The control number.
        """

        field = Field(tag='001', data=control_number)
        self.add_field(field)

    def set_author(self, author):

        """
        Set 100.

        Args:
            author (str): The author.
        """

        field = Field(
            tag='100',
            indicators=['0', '1'],
            subfields=['a', author]
        )

        self.add_field(field)

    def set_title(self, title):

        """
        Set 245.

        Args:
            title (str): The title.
        """

        field = Field(
            tag='245',
            indicators=['0', '1'],
            subfields=['a', title]
        )

        self.add_field(field)

    def set_publisher(self, publisher, pubyear):

        """
        Set 260 b.

        Args:
            publisher (str): The publisher.
            pubyear (str): The pubyear.
        """

        field = Field(
            tag='260',
            indicators=['0', '1'],
            subfields=[
                'b', publisher,
                'c', pubyear
            ]
        )

        self.add_field(field)

    def set_pubyear(self, pubyear):

        """
        Set 264 c.

        Args:
            year (str): The year.
        """

        field = Field(
            tag='264',
            indicators=['0', '1'],
            subfields=['c', pubyear]
        )

        self.add_field(field)


class Mock_HLOM(Mock_Corpus):

    @contextmanager
    def writer(self, data_file):

        """
        Yield a MARCWriter instance.

        Args:
            data_file (str): The file basename.
        """

        path = os.path.join(self.path, data_file)

        with open(path, 'ab') as fh:
            yield MARCWriter(fh)

    def add_marc(self,
        data_file='hlom',
        control_number=None,
        title='title',
        author='author',
        publisher='publisher',
        pubyear='pubyear',
    ):

        """
        Add a MARC record to a .dat file.

        Args:
            data_file (str): The file name.
            control_number (str): The control number.
            author (str): The author.
            title (str): The title.
            publisher (str): The publisher.
            pubyear (str): The date.

        Returns:
            pymarc.Record
        """

        # Use a random uuid, if no CN.
        if not control_number:
            control_number = str(uuid.uuid4())

        with self.writer(data_file) as writer:

            marc = Mock_MARC()

            marc.set_control_number(control_number)

            if author:
                marc.set_author(author)

            if title:
                marc.set_title(title)

            if publisher and pubyear:
                marc.set_publisher(publisher, pubyear)

            writer.write(marc)

            return marc
