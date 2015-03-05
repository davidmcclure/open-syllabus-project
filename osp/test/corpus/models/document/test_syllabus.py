

def test_1(Document, config):

    """
    TODO|dev
    """

    config.config.update_w_merge({
        'osp': {
            'corpus': 'test'
        }
    })

    assert config['osp']['corpus'] == 'test'


def test_2(Document, config):

    """
    TODO|dev
    """

    assert config['osp']['corpus'] != 'test'
