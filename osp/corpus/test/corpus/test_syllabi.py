

import os

from osp.corpus.corpus import Corpus
from osp.corpus.syllabus import Syllabus
from osp.corpus.utils import int_to_dir


def test_syllabi(mock_corpus):

    """
    Corpus#syllabi() should generate Syllabus instances for all files.
    """

    # Add 10 segments.
    mock_corpus.add_segments(s1=0, s2=10)
    corpus = Corpus(mock_corpus.path)

    # Add 10 files per segment.
    for i in range(0, 10):
        segment = int_to_dir(i)
        mock_corpus.add_files(segment, 10, prefix=segment+'-')

    syllabi = corpus.syllabi()

    # Walk segments:
    for i in range(0, 10):

        segment = int_to_dir(i)

        # Walk files:
        for j in range(0, 10):

            # Should be a Syllabus instance.
            syllabus = next(syllabi)
            assert isinstance(syllabus, Syllabus)

            # Should wrap the right file.
            name = segment+'-'+str(j)
            path = os.path.join(corpus.path, segment, name)
            assert syllabus.path == path
