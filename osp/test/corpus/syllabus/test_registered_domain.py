

from osp.corpus.syllabus import Syllabus


def test_regular_url(mock_osp):

    """
    Syllabys#registered_domain should return the "base" URL.
    """

    log = {'url': 'http://www.yale.edu/syllabus.pdf'}

    path = mock_osp.add_file(log=log)
    syllabus = Syllabus(path)

    assert syllabus.registered_domain == 'yale.edu'


def test_double_url(mock_osp):

    """
    Many documents in the corpus are scraped from archive.org, which means
    that many URLs take the form of:

    https://web.archive.org/web/<id>/http://original-url.org

    In this case, we want the domain from the second, "original" URL.
    """

    url1 = 'https://web.archive.org/web/123'
    url2 = 'http://www.yale.edu/syllabus.pdf'

    path = mock_osp.add_file(log={'url': url1+'/'+url2})
    syllabus = Syllabus(path)

    assert syllabus.registered_domain == 'yale.edu'
