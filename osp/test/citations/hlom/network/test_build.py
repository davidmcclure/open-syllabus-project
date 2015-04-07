

from osp.citations.hlom.models.citation import HLOM_Citation
from osp.citations.hlom.network import Network


def test_build(models, add_hlom, add_doc):

    # 5 HLOM texts.
    t1 = add_hlom(control_number='1')
    t2 = add_hlom(control_number='2')
    t3 = add_hlom(control_number='3')
    t4 = add_hlom(control_number='4')
    t5 = add_hlom(control_number='5')

    # 3 syllabi.
    s1 = add_doc('s1')
    s2 = add_doc('s2')
    s3 = add_doc('s3')

    # texts 1-3 in s1.
    HLOM_Citation.create(document=s1, record=t1)
    HLOM_Citation.create(document=s1, record=t2)
    HLOM_Citation.create(document=s1, record=t3)

    # texts 2-4 in s2.
    HLOM_Citation.create(document=s2, record=t2)
    HLOM_Citation.create(document=s2, record=t3)
    HLOM_Citation.create(document=s2, record=t4)

    # texts 3-5 in s3.
    HLOM_Citation.create(document=s3, record=t3)
    HLOM_Citation.create(document=s3, record=t4)
    HLOM_Citation.create(document=s3, record=t5)

    network = Network()
    network.build()
