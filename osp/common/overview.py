

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


    def put_store_object(self, i_long, i_string, json):

        """
        Set a store object

        :param i_long: An indexed numeric field.
        :param i_string: An indexed string field.
        :param json: JSON for the object.
        """

        pass


    def get_store_object(self, id):

        """
        Retrieve a store object

        :param id: The object id.
        """

        pass


    def delete_store_object(self, id):

        """
        Delete a store object

        :param id: The object id.
        """

        pass
