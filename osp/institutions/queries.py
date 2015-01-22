

from osp.institutions.models.institution import Institution
from osp.locations.models.doc_inst import Document_Institution as DocInst
from osp.institutions.models.lonlat import Institution_LonLat as LonLat
from peewee import *


def store_objects():

    """
    Join lon/lats, and just select institutions that have been matched with a
    document in the corpus.
    """

    return (
        Institution
        .select(
            Institution,
            LonLat.lon,
            LonLat.lat
        )
        .distinct([Institution.id])
        .join(LonLat)
        .switch(Institution)
        .join(DocInst)
        .order_by(
            Institution.id,
            LonLat.created.desc()
        )
    )


def csv_rows():

    """
    Join lon/lats for a Fusion Tables CSV.
    """

    return (
        Institution
        .select(
            Institution,
            LonLat.lon,
            LonLat.lat
        )
        .distinct([Institution.id])
        .join(LonLat)
        .order_by(
            Institution.id,
            LonLat.created.desc()
        )
    )
