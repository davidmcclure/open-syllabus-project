

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
