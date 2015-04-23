

import os

from osp.common.config import config
from osp.institutions.models.institution import Institution
from geopy.geocoders import OpenMapQuest


def geocode(id):

    """
    Geocode an institution.

    Args:
        id (int): The institution id.
    """

    coder = OpenMapQuest(config['mapquest']['api_key'])
    inst = Institution.get(Institution.id==id)

    # Geocode.
    location = coder.geocode(inst.geocoding_query, timeout=10)

    if location:

        # Write the coordinate.
        inst.metadata['Latitude']  = location.latitude
        inst.metadata['Longitude'] = location.longitude
        inst.save()
