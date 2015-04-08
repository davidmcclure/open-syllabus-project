

from osp.citations.hlom.models.citation import HLOM_Citation
from osp.citations.hlom.network import Network


def test_build(models, add_hlom, add_doc):
    pass

    ## 5 HLOM texts.
    #t1 = add_hlom(control_number='cn1', title='title1', author='author1')
    #t2 = add_hlom(control_number='cn2', title='title2', author='author2')
    #t3 = add_hlom(control_number='cn3', title='title3', author='author3')
    #t4 = add_hlom(control_number='cn4', title='title4', author='author4')
    #t5 = add_hlom(control_number='cn5', title='title5', author='author5')
    #t6 = add_hlom(control_number='cn6', title='title6', author='author6')

    ## 3 syllabi.
    #s1 = add_doc('s1')
    #s2 = add_doc('s2')
    #s3 = add_doc('s3')

    ## texts 1-4 in s1.
    #HLOM_Citation.create(document=s1, record=t1)
    #HLOM_Citation.create(document=s1, record=t2)
    #HLOM_Citation.create(document=s1, record=t3)
    #HLOM_Citation.create(document=s1, record=t4)

    ## texts 2-5 in s2.
    #HLOM_Citation.create(document=s2, record=t2)
    #HLOM_Citation.create(document=s2, record=t3)
    #HLOM_Citation.create(document=s2, record=t4)
    #HLOM_Citation.create(document=s2, record=t5)

    ## texts 3-6 in s3.
    #HLOM_Citation.create(document=s3, record=t3)
    #HLOM_Citation.create(document=s3, record=t4)
    #HLOM_Citation.create(document=s3, record=t5)
    #HLOM_Citation.create(document=s3, record=t6)

    #n = Network()
    #n.build()

    ## Should add nodes.
    #for i in [str(i) for i in range(1, 6)]:
        #assert n.graph.node['cn'+i] == {
            #'title': 'title'+i, 'author': 'author'+i
        #}

    #assert n.graph.edge['cn1']['cn2']['weight'] == 1
    #assert n.graph.edge['cn2']['cn3']['weight'] == 2
    #assert n.graph.edge['cn3']['cn4']['weight'] == 3
    #assert n.graph.edge['cn4']['cn5']['weight'] == 2
    #assert n.graph.edge['cn5']['cn6']['weight'] == 1
