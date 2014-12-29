

from osp.institutions.models.institution import Institution
from osp.institutions.models.lonlat import LonLat
from peewee import *


def join_lonlats():

    """
    Join the most recent lon-lat values onto the institutions.
    """

    return (
        Institution
        .select(Institution, LonLat.lon, LonLat.lat)
        .distinct([Institution.id])
        .join(LonLat, JOIN_LEFT_OUTER)
        .order_by(Institution.id, LonLat.created.desc())
    )
