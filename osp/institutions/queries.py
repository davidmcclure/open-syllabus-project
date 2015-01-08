

from osp.institutions.models.institution import Institution
from osp.locations.models.doc_inst import Document_Institution as DocInst
from osp.institutions.models.lonlat import Institution_LonLat as LonLat
from peewee import *


def store_objects():

    """
    Join lonlats, and just select institutions that have been matched with a
    document in the corpus.
    """

    return (
        Institution
        .select(
            Institution,
            Lonlat.lon,
            Lonlat.lat
        )
        .distinct([Institution.id])
        .join(Lonlat)
        .switch(Institution)
        .join(DocInst)
        .order_by(
            Institution.id,
            Lonlat.created.desc()
        )
    )
