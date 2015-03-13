

from osp.citations.hlom.utils import sanitize_query


def test_sanitize_query():

    """
    Lucene reserved characters should be escaped.
    """

    assert sanitize_query('abc + def') == r'abc \+ def'
    assert sanitize_query('abc - def') == r'abc \- def'
    assert sanitize_query('abc & def') == r'abc \& def'
    assert sanitize_query('abc | def') == r'abc \| def'
    assert sanitize_query('abc ! def') == r'abc \! def'
    assert sanitize_query('abc ( def') == r'abc \( def'
    assert sanitize_query('abc ) def') == r'abc \) def'
    assert sanitize_query('abc { def') == r'abc \{ def'
    assert sanitize_query('abc } def') == r'abc \} def'
    assert sanitize_query('abc [ def') == r'abc \[ def'
    assert sanitize_query('abc ] def') == r'abc \] def'
    assert sanitize_query('abc ^ def') == r'abc \^ def'
    assert sanitize_query('abc " def') == r'abc \" def'
    assert sanitize_query('abc ~ def') == r'abc \~ def'
    assert sanitize_query('abc * def') == r'abc \* def'
    assert sanitize_query('abc ? def') == r'abc \? def'
    assert sanitize_query('abc : def') == r'abc \: def'
    assert sanitize_query('abc \ def') == r'abc \\ def'
    assert sanitize_query('abc / def') == r'abc \/ def'
