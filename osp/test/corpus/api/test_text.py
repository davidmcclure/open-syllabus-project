

def test_text(api_client):

    """
    The /text endpoint should queue the job that then queues the individual
    text extraction jobs for each document.
    """

    ping = api_client.post('/corpus/text', data={'o1':1, 'o2':5})
    # TODO
