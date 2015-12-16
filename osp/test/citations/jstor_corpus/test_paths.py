

import os

from osp.citations.jstor_corpus import JSTOR_Corpus


def test_generate_paths(models, mock_jstor):

    """
    JSTOR_Corpus#paths() should generate manifest paths.
    """

    paths = [
        mock_jstor.add_article(),
        mock_jstor.add_article(),
        mock_jstor.add_article(),
    ]

    corpus = JSTOR_Corpus(mock_jstor.path)
    output = list(corpus.paths())

    assert set(output) == set(paths)
    assert len(output) == 3


def test_ignore_non_xml_files(models, mock_jstor):

    """
    JSTOR_Corpus#paths() should generate manifest paths.
    """

    # 3 XML manifests.
    paths = [
        mock_jstor.add_article(),
        mock_jstor.add_article(),
        mock_jstor.add_article(),
    ]

    dirname = os.path.dirname(list(paths)[0])

    # 3 non-XML files.
    for ext in ['js', 'zip', 'txt']:
        with open(os.path.join(dirname, 'test.'+ext), 'w') as fh:
            print('content', file=fh)

    corpus = JSTOR_Corpus(mock_jstor.path)
    output = list(corpus.paths())

    assert set(output) == set(paths)
    assert len(output) == 3
