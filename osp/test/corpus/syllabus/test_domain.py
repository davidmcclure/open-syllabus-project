

import pytest

from osp.corpus.syllabus import Syllabus


@pytest.mark.parametrize('url,domain', [

    # http
    (
        'http://www.yale.edu/syllabus.pdf',
        'yale.edu',
    ),

    # https
    (
        'https://www.yale.edu/syllabus.pdf',
        'yale.edu',
    ),

    # web archive + http
    (
        'https://web.archive.org/web/123/http://www.yale.edu/syllabus.pdf',
        'yale.edu',
    ),

    # web archive + https
    (
        'https://web.archive.org/web/123/https://www.yale.edu/syllabus.pdf',
        'yale.edu',
    ),

])
def test_domain(url, domain, mock_osp):

    path = mock_osp.add_file(log=dict(url=url))
    syllabus = Syllabus(path)

    assert syllabus.domain == domain
