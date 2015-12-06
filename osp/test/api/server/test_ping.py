

def test_ping(api_client):

    """
    /ping should return 200.
    """

    r = api_client.get('/ping')
    assert r.status_code == 200
