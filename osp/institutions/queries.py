

from osp.locations.models.doc_inst import DocInst
from osp.institutions.models.institution import Institution
from osp.institutions.models.institution_lonlat import InstitutionLonlat
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
            InstitutionLonlat.lon,
            InstitutionLonlat.lat
        )
        .distinct([Institution.id])
        .join(InstitutionLonlat)
        .switch(Institution)
        .join(DocInst)
        .order_by(
            Institution.id,
            InstitutionLonlat.created.desc()
        )
    )
