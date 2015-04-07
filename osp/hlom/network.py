

from osp.citations.hlom.models.citation import HLOM_Citation


class Network:


    @classmethod
    def from_gml(cls, file_path):

        """
        Hydrate the network from a GML file.

        Args:
            file_path (str)

        Returns:
            Network
        """

        pass


    def __init__(self, graph=None):

        """
        Set the graph instance.

        Args:
            graph (networkx.Graph)
        """

        self.graph = graph


    def build(self):

        """
        Build the network from the citation table.
        """

        pass


    def write_gml(self):

        """
        Serialize the graph as GML.
        """

        pass
