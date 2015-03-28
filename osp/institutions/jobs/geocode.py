

import os

from osp.institutions.models.institution import Institution
from geopy.geocoders import Nominatim


coder = Nominatim()


def geocode(id):

    """
    Geocode an institution.

    Args:
        id (int): The institution id.
    """

    row = Institution.get(Institution.id==id)

    # Geocode.
    location = coder.geocode(row.geocoding_query, timeout=10)

    if location:

        # Write the coordinate.
        row.metadata['Latitude']  = location.latitude
        row.metadata['Longitude'] = location.longitude
        row.save()
