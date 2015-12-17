

import requests
import re
import random


class Faker:


    def __init__(self, text_url):

        """
        Load and clean a text URL.

        Args:
            text_url (str)
        """

        r = requests.get(text_url)

        self.text = re.sub('\s{2,}', ' ', r.text).strip()


    def snippet(self, length):

        """
        Get a random text snippet.

        Args:
            length (int)
        """

        start = random.randrange(0, len(self.text)-length)

        return self.text[start:start+length]
