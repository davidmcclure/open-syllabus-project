

import os
import requests
import click

from osp.common.config import config
from osp.api.utils import print_code
from boto import ec2


class Client:


    def __init__(self):

        """
        Initialize the EC2 connection.
        """

        self.conn = ec2.connect_to_region(config['ec2']['region'])


    def filter_ips(self, filters):

        """
        Get a list of filtered IP addresses.

        Args:
            filters (dict)

        Return: list
        """

        ips = []
        for r in self.conn.get_all_reservations(filters=filters):
            ips += [i.ip_address for i in r.instances]

        return ips


    @property
    def worker_ips(self):

        """
        Get a list of worker IP addresses.
        """

        return self.filter_ips({
            'tag:osp': 'worker',
            'tag:user': config['ec2']['namespace'],
        })


    @property
    def worker_urls(self):

        """
        Get a list of worker URLs.
        """

        return ['http://'+ip for ip in self.worker_ips]


    def queue(self, model, job):

        """
        Queue a job against a model.

        Args:
            model (str) - Model import path.
            job (str) - Job import path.
        """

        pass


    def ping(self):

        """
        Ping the workers.
        """

        for url in self.worker_urls:

            r = requests.get(url+'/ping')

            click.echo(url)
            print_code(r.status_code)


    def status(self):

        """
        List pending/failed counts for each worker.
        """

        pass


    def requeue(self):

        """
        Requeue all tasks in all workers.
        """

        pass
