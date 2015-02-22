

import os
import requests
import ijson

from base64 import urlsafe_b64encode as b64
from jsonstream.pyjsonstream import JSONStream
from osp.common.config import config


class Overview:


    @classmethod
    def from_env(cls):

        """
        Get an instance from the ENV params.
        """

        return cls(
            config['overview']['api_url'],
            config['overview']['api_token'],
            config['overview']['set_id']
        )


    def __init__(self, url, token, set_id):

        """
        Initialize the session, set headers.

        :param url: The API endpoint.
        :param token: The API token.
        :param set_id: The document set ID.
        """

        self.url = url.rstrip('/')
        self.token = token
        self.set_id = set_id

        # Initialize the session.
        self.overview = requests.Session()
        self.overview.headers.update(self.headers)


    @property
    def headers(self):

        """
        Build the shared header.
        """

        token = (self.token+':x-auth-token').encode('ascii')
        value = b64(token).decode('utf-8')

        return {'Authorization': 'Basic '+value}


    # URL builders:
    # -------------


    @property
    def documents_url(self):
        return self.url+'/document-sets/'+str(self.set_id)+'/documents'


    def document_url(self, doc_id):
        return self.documents_url()+'/'+str(doc_id)


    @property
    def state_url(self):
        return self.url+'/store/state'


    @property
    def objects_url(self):
        return self.url+'/store/objects'


    def object_url(self, id):
        return self.objects_url+'/'+str(id)


    @property
    def document_objects_url(self):
        return self.url+'/store/document-objects'


    @property
    def document_object_counts_url(self):
        return self.document_objects_url+'/count-by-object'


    # API wrappers:
    # -------------


    def list_documents(self, params={}):

        """
        Get a list of documents.

        :param params: Query parameters.
        """

        return self.overview.get(
            self.documents_url, params=params
        )


    def stream_documents(self, params={}):

        """
        Stream all documents.

        :param params: Query parameters.
        """

        params.update({'stream': 'true'})

        request = self.overview.get(
            self.documents_url, params=params, stream=True
        )

        for doc in ijson.items(request.raw, 'items.item'):
            yield doc


    def get_document(self, doc_id):

        """
        Get a list of documents.

        :param doc_id: The document ID.
        """

        return self.overview.get(self.document_url(doc_id))


    def put_state(self, state):

        """
        Set the store state.

        :param state: The new state.
        """

        return self.overview.put(self.state_url, json=state)


    def get_state(self):

        """
        Retrieve the store state.
        """

        return self.overview.get(self.state_url)


    def post_object(self, obj):

        """
        Set a store object

        :param obj: A store object (or array of objects).
        """

        return self.overview.post(self.objects_url, json=obj)


    def list_objects(self):

        """
        Get all store objects.
        """

        return self.overview.get(self.objects_url)


    def count_objects(self):

        """
        Count the number of store objects.
        """

        return len(self.list_objects().json())


    def get_object(self, id):

        """
        Retrieve a store object

        :param id: The object id.
        """

        return self.overview.get(self.object_url(id))


    def delete_object(self, id):

        """
        Delete a store object

        :param id: The object id.
        """

        return self.overview.delete(self.object_url(id))


    def post_document_objects(self, links):

        """
        Create object->document links.

        :param links: An array of [docId, objId] pairs.
        """

        return self.overview.post(
            self.document_objects_url, json=links
        )


    def list_document_object_counts(self, params={}):

        """
        For each store object, get the number of referenced docs.

        :param params: Query parameters.
        """

        return self.overview.get(
            self.document_object_counts_url, params=params
        )


    def delete_document_objects(self, links):

        """
        Delete object->document links.

        :param links: An array of [docId, objId] pairs.
        """

        return self.overview.delete(
            self.document_objects_url, json=links
        )
