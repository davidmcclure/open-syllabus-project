

from peewee import *
from osp.citations.hlom.models.citation import HLOM_Citation
from osp.citations.hlom.models.record import HLOM_Record


def text_counts():

    """
    Get an ordered list of MARC control number -> citation counts.
    """

    count = fn.Count(HLOM_Citation.id)

    return (
        HLOM_Citation
        .select(
            HLOM_Citation.record,
            count.alias('count')
        )
        .group_by(HLOM_Citation.record)
        .distinct(HLOM_Citation.record)
        .order_by(count.desc())
    )


def syllabus_counts():

    """
    Get an ordered list of document paths -> citation counts.
    """

    count = fn.Count(HLOM_Citation.id)

    return (
        HLOM_Citation
        .select(
            HLOM_Citation.document,
            count.alias('count')
        )
        .group_by(HLOM_Citation.document)
        .distinct(HLOM_Citation.document)
        .order_by(count.desc())
    )


def records_with_citations():

    """
    Get all HLOM records that have at least one citation, annotated with the
    citation count.
    """

    count = fn.Count(HLOM_Citation.id)

    return (
        HLOM_Record
        .select(
            HLOM_Record,
            count.alias('count')
        )
        .join(
            HLOM_Citation,
            on=(HLOM_Record.control_number==HLOM_Citation.record)
        )
        .group_by(HLOM_Record)
    )
