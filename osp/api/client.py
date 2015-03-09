

class Client:


    def __init__(self, inventory):

        """
        Set the EC2 interface.

        Args:
            inventory (Inventory): The EC2 adapter.
        """

        self.inventory = inventory


    def queue(route, total):

        """
        Dispatch partition orders to EC2 workers.

        Args:
            route (str): The API endpoint.
            total (int): The total number of objects.

        Yields:
            tuple: (response, offset 1, offset 2)
        """

        urls = self.inventory.worker_urls
        pts = partitions(total, len(urls))

        for i, url in enumerate(urls):

            o1 = pts[i][0]
            o2 = pts[i][1]

            # Post the boundaries.
            r = requests.post(
                url+route,
                params={'o1': o1, 'o2': o2}
            )

            yield (r, o1, o2)
