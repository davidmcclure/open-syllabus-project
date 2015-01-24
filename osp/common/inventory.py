

import os

from boto import ec2


class Inventory:


    def __init__(self):

        """
        Initialize the EC2 connection.
        """

        self.conn = ec2.connect_to_region(os.environ['OSP_REGION'])


    @property
    def worker_ips(self):

        """
        Get a list of worker IP addresses.
        """

        ips = []
        for r in self.conn.get_all_reservations():
            for i in r.instances:
                if i.tags.get('osp', False) == 'worker':
                    ips.append(i.ip_address)

        return ips


    @property
    def worker_urls(self):

        """
        Get a list of worker URLs.
        """

        return ['http://'+ip for ip in self.worker_ips]
