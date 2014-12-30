

from osp.locations.models.doc_inst import DocInst
from osp.institutions.models.institution import Institution
from osp.institutions.models.lonlat import LonLat
from peewee import *


def store_objects():

    """
    Join lonlats, and just select institutions that have been matched with a
    document in the corpus.
    """

    return (
        Institution
        .select(Institution, LonLat.lon, LonLat.lat)
        .distinct([Institution.id])
        .join(LonLat)
        .switch(Institution)
        .join(DocInst)
        .order_by(Institution.id, LonLat.created.desc())
    )
