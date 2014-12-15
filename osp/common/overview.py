

import os
import requests
import json

from base64 import urlsafe_b64encode as b64


class Overview:


    def __init__(self, key=None):

        """
        Set the store state.

        :param key: The API key.
        """

        # Set the URL and API token.
        self.key = key if key else os.environ['OSP_API_KEY']
        self.url = os.environ['OSP_API_URL'].rstrip('/')

        # Initialize the session.
        self.overview = requests.Session()
        self.overview.headers.update(self.headers)


    @property
    def headers(self):

        """
        Build the shared header.
        """

        token = (self.key+':x-auth-token').encode('ascii')
        value = b64(token).decode('utf-8')

        return {'Authorization': 'Basic '+value}


    @property
    def store_state_url(self):

        """
        Store state API endpoint.
        """

        return self.url+'/store/state'


    @property
    def store_objects_url(self):

        """
        Store objects API endpoint.
        """

        return self.url+'/store/objects'


    def store_object_url(self, id):

        """
        Individual store object API endpoint.

        :param id: The object id.
        """

        return self.store_objects_url+'/'+str(id)


    def put_store_state(self, state):

        """
        Set the store state.

        :param state: The new state.
        """

        return self.overview.put(self.store_state_url, json=state)


    def get_store_state(self):

        """
        Retrieve the store state.
        """

        return self.overview.get(self.store_state_url).json()


    def post_store_object(self, obj):

        """
        Set a store object

        :param obj: A store object (or array of objects).
        """

        return self.overview.post(self.store_objects_url, json=obj).json()


    def get_store_object(self, id):

        """
        Retrieve a store object

        :param id: The object id.
        """

        return self.overview.get(self.store_object_url(id)).json()


    def delete_store_object(self, id):

        """
        Delete a store object

        :param id: The object id.
        """

        return self.overview.delete(self.store_object_url(id)).ok
