

from osp.institutions.models.institution import Institution
from peewee import *

from osp.institutions.models.institution_lonlat \
    import InstitutionLonlat as LonLat

from osp.locations.models.document_institution \
    import DocumentInstitution as DocInst


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
