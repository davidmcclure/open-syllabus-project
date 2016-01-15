

import pytest


@pytest.mark.parametrize('title,surname,unfocused', [

    # Focused
    ('Open Syllabus Project', 'McClure', False),

    # Unfocused
    ('Ideas', 'Young', True),

])
def test_unfocused(title, surname, unfocused, add_text):

    text = add_text(surname=surname, title=title)

    assert text.unfocused(0.1) == unfocused


def test_allow_unfocused_duplicates(add_text):

    """
    If a text is a duplicate, return unfocused, since we're using duplication
    as a crude signal for significance / canonicity.
    """

    t1 = add_text(surname='Young', title='Ideas', duplicate=False)
    t2 = add_text(surname='Young', title='Ideas', duplicate=True)

    assert t1.unfocused(0.1) == True
    assert t2.unfocused(0.1) == False
