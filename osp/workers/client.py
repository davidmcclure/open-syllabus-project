

import os
import requests
import click

from osp.common.config import config
from osp.workers.utils import print_code

from boto import ec2
from blessings import Terminal


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
            ips += [i.ip_address for i in r.instances if i.ip_address]

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


    def ping(self):

        """
        Ping the workers.
        """

        for url in self.worker_urls:

            r = requests.get(url+'/ping')

            click.echo(url)
            print_code(r.status_code)


    def queue(self, model_import, job_import):

        """
        Queue a job against a model.

        Args:
            model_import (str): Model import path.
            job_import (str): Job import path.
        """

        worker_count = len(self.worker_urls)

        for i, url in enumerate(self.worker_urls):

            r = requests.post(url+'/queue', data=dict(
                model_import    = model_import,
                job_import      = job_import,
                worker_count    = worker_count,
                offset          = i,
            ))

            click.echo(url)
            print_code(r.status_code)


    def clear(self):

        """
        Clear all queues in all workers.
        """

        for url in self.worker_urls:

            click.echo(url)

            # Default:
            r1 = requests.post(url+'/rq/queue/default/empty')
            print_code(r1.status_code)

            # Failed:
            r1 = requests.post(url+'/rq/queue/failed/empty')
            print_code(r1.status_code)


    def status(self):

        """
        List pending/failed counts for each worker.
        """

        term = Terminal()

        for url in self.worker_urls:

            click.echo(url)

            # Get the queue counts.
            r = requests.get(url+'/rq/queues.json')

            for queue in r.json()['queues']:

                # Pending jobs:
                if queue['name'] == 'default':
                    click.echo(term.green(str(queue['count'])))

                # Failed jobs:
                if queue['name'] == 'failed':
                    click.echo(term.red(str(queue['count'])))


    def requeue(self):

        """
        Requeue all tasks in all workers.
        """

        for url in self.worker_urls:

            click.echo(url)

            r = requests.post(url+'/rq/requeue-all')
            print_code(r.status_code)
