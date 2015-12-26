

import pytest


pytestmark = pytest.mark.usefixtures('db', 'es')
