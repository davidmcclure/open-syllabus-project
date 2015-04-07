

import numpy as np

from osp.citations.hlom.models.record import HLOM_Record
from osp.citations.hlom.models.citation import HLOM_Citation


def test_es_index(models, config, add_hlom, add_doc, hlom_index):

    """
    HLOMIndex.index() should index cited records in Elasticsearch.
    """

    r1 = add_hlom(
        author      ='author1',
        title       ='title1',
        publisher   ='publisher1',
        pubyear     ='pubyear1'
    )

    r2 = add_hlom(
        author      ='author2',
        title       ='title2',
        publisher   ='publisher2',
        pubyear     ='pubyear2'
    )

    r3 = add_hlom(
        author      ='author3',
        title       ='title3',
        publisher   ='publisher3',
        pubyear     ='pubyear3'
    )


    # 1 citation for r1.
    d1 = add_doc('content1')
    HLOM_Citation.create(record=r1, document=d1)

    # 2 citations for r2.
    d2 = add_doc('content2')
    d3 = add_doc('content3')
    HLOM_Citation.create(record=r2, document=d2)
    HLOM_Citation.create(record=r2, document=d3)

    # 3 citations for r3.
    d4 = add_doc('content4')
    d5 = add_doc('content5')
    d6 = add_doc('content6')
    HLOM_Citation.create(record=r3, document=d4)
    HLOM_Citation.create(record=r3, document=d5)
    HLOM_Citation.create(record=r3, document=d6)

    HLOM_Record.write_stats()
    HLOM_Record.write_metrics()
    HLOM_Record.es_insert()

    assert HLOM_Record.es_count() == 3

    doc1 = config.es.get('hlom', r1.control_number)

    assert doc1['_source']['author']    == 'author1'
    assert doc1['_source']['title']     == 'title1'
    assert doc1['_source']['publisher'] == 'publisher1'
    assert doc1['_source']['pubyear']   == 'pubyear1'
    assert doc1['_source']['count']     == 1
    assert doc1['_source']['rank']      == 3
    assert doc1['_source']['percent']   == 0

    doc2 = config.es.get('hlom', r2.control_number)

    # Get the middle-document percentile.
    pct = ((np.log(3)-np.log(2))/np.log(3))*100

    assert doc2['_source']['author']    == 'author2'
    assert doc2['_source']['title']     == 'title2'
    assert doc2['_source']['publisher'] == 'publisher2'
    assert doc2['_source']['pubyear']   == 'pubyear2'
    assert doc2['_source']['count']     == 2
    assert doc2['_source']['rank']      == 2
    assert doc2['_source']['percent']   == pct

    doc3 = config.es.get('hlom', r3.control_number)

    assert doc3['_source']['author']    == 'author3'
    assert doc3['_source']['title']     == 'title3'
    assert doc3['_source']['publisher'] == 'publisher3'
    assert doc3['_source']['pubyear']   == 'pubyear3'
    assert doc3['_source']['count']     == 3
    assert doc3['_source']['rank']      == 1
    assert doc3['_source']['percent']   == 100
