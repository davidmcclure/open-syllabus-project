

import os

from geopy.geocoders import Nominatim
from osp.institutions.models.lonlat import Institution_LonLat


def geocode(iid, query):

    """
    Geocode a query, write the lon/lat to Postgres.

    :param int iid: The institution id.
    :param str query: The query for the geocoder.
    """

    coder = Nominatim()

    # Geocode.
    location = coder.geocode(query, timeout=10)

    if location:

        # Write the coordinate.
        Institution_LonLat.create(
            institution=iid,
            lat=location.latitude,
            lon=location.longitude
        )
