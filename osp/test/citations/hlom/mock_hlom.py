

import os
import tempfile
import shutil

from osp.citations.hlom.models.record import HLOM_Record
from contextlib import contextmanager
from pymarc import Record, Field, MARCWriter


def get_marc(number, title, author):

    """
    Create a MARC record.

    Args:
        number (str): The control number.
        title (str): The title.
        author (str): The author.

    Returns:
        pymarc.Record
    """

    marc = Record()

    f001 = Field(tag='001', data=number)

    f100 = Field(
        tag='100',
        indicators=['0', '1'],
        subfields=['a', author]
    )

    f245 = Field(
        tag='245',
        indicators=['0', '1'],
        subfields=['a', title]
    )

    marc.add_field(f001)
    marc.add_field(f100)
    marc.add_field(f245)

    return marc


def get_hlom(number, title, author):

    """
    Insert a HLOM record row.

    Args:
        number (str): The control number.
        title (str): The title.
        author (str): The author.

    Returns:
        HLOM_Record
    """

    marc = get_marc(number, title, author)

    return HLOM_Record.create(
        control_number=number,
        record=marc.as_marc()
    )


class MockHLOM:


    def __init__(self):

        """
        Create the temporary directory.
        """

        self.path = tempfile.mkdtemp()


    @contextmanager
    def writer(self, segment):

        """
        Yield a MARCWriter instance.

        Args:
            segment (str): The file basename.
        """

        path = os.path.join(self.path, segment+'.dat')

        with open(path, 'ab') as fh:
            yield MARCWriter(fh)


    def add_marc(self, segment, number, title='', author=''):

        """
        Add a MARC record to a .dat file.

        Args:
            segment (str): The file basename.
            number (str): The control number.
            title (str): The title.
            author (str): The author.

        Returns:
            pymarc.Record
        """

        with self.writer(segment) as writer:

            marc = Record()

            f001 = Field(
                tag='001',
                data=number
            )

            f100 = Field(
                tag='100',
                indicators=['0', '1'],
                subfields=['a', author]
            )

            f245 = Field(
                tag='245',
                indicators=['0', '1'],
                subfields=['a', title]
            )

            marc.add_field(f001)
            marc.add_field(f100)
            marc.add_field(f245)

            writer.write(marc)
            return marc


    def teardown(self):

        """
        Delete the temporary directory.
        """

        shutil.rmtree(self.path)
