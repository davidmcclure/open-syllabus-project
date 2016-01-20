

import pytest


@pytest.mark.parametrize('title,surname,unfocused', [

    # Focused
    ('Open Syllabus Project', 'McClure', False),

    # Unfocused
    ('Ideas', 'Young', True),

])
def test_unfocused(title, surname, unfocused, add_text):

    text = add_text(surname=surname, title=title)

    assert text.unfocused(max_fuzz=0.1) == unfocused


def test_whitelist(add_text):

    """
    When a list of whitelisted ids is passed, allow any texts in the list that
    fall above the fuzziness threshold.
    """

    t1 = add_text(surname='Ideas', title='Young')
    t2 = add_text(surname='Ideas', title='Young')
    t3 = add_text(surname='Ideas', title='Young')

    whitelist = [t1.id, t2.id]

    assert t1.unfocused(max_fuzz=0.1, whitelist=whitelist) == False
    assert t2.unfocused(max_fuzz=0.1, whitelist=whitelist) == False
    assert t3.unfocused(max_fuzz=0.1, whitelist=whitelist) == True
