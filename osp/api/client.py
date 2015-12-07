

import os

from boto import ec2


class Client:


    def __init__(self):

        """
        Initialize the EC2 connection.
        """

        self.conn = ec2.connect_to_region(os.environ['OSP_REGION'])


    def ips_by_tag(self, key, value):

        """
        Get a list of IP addresses by tag.

        :param key: The tag key.
        :param value: The tag value.
        """

        ips = []
        for r in self.conn.get_all_reservations():
            for i in r.instances:
                if i.tags.get(key, False) == value and i.ip_address:
                    ips.append(i.ip_address)

        return ips


    @property
    def worker_ips(self):

        """
        Get a list of worker IP addresses.
        """

        return self.ips_by_tag('osp', 'worker')


    @property
    def worker_urls(self):

        """
        Get a list of worker URLs.
        """

        return ['http://'+ip for ip in self.worker_ips]
