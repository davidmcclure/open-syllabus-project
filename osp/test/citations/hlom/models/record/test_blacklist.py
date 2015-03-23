

from osp.citations.hlom.models.record import HLOM_Record


def test_blacklist(models, add_hlom):

    """
    When a record is blacklisted, set a `blacklisted=True` key on the record's
    metadata, which will block it from being indexed in Elasticsearch.
    """

    record = add_hlom()

    HLOM_Record.blacklist(record.control_number)

    record = HLOM_Record.reload(record)
    assert record.metadata['blacklisted'] == True
