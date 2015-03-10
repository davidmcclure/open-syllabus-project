

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

        pass
