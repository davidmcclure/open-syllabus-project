

import os
import tempfile
import shutil
import uuid

from osp.citations.models import Text
from contextlib import contextmanager
from pymarc import Record, Field, MARCWriter


class MockMARC(Record):


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


class MockHLOM:


    def __init__(self):

        """
        Create the temporary directory.
        """

        self.path = tempfile.mkdtemp()


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


    def add_marc(self, title='title', author='author',
                 publisher='publisher', pubyear='pubyear',
                 data_file='hlom', control_number=None):

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

            marc = MockMARC()
            marc.set_control_number(control_number)
            marc.set_author(author)
            marc.set_title(title)
            marc.set_publisher(publisher, pubyear)

            writer.write(marc)
            return marc


    def teardown(self):

        """
        Delete the temporary directory.
        """

        shutil.rmtree(self.path)
