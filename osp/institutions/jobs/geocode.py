

import os

from geopy.geocoders import MapQuest
from osp.institutions.models.lonlat import Institution_LonLat


def geocode(iid, key, query):

    """
    Geocode a query, write the lon/lat to Postgres.

    :param int iid: The institution id.
    :param str key: A MapQuest API key.
    :param str query: The query for the geocoder.
    """

    coder = MapQuest(key)

    # Geocode.
    g = coder.geocode(query, timeout=10)

    # Write the coordinate.
    Institution_LonLat.create(
        institution=iid, lon=g.longitude, lat=g.latitude
    )
