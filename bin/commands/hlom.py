

import click
import sys
import csv

from osp.common.models.base import pg_local, pg_remote, redis
from osp.common.overview import Overview
from osp.common.utils import query_bar, grouper
from osp.citations.hlom.models.record import HLOM_Record
from osp.citations.hlom.models.citation import HLOM_Citation
from osp.citations.hlom.dataset import Dataset
from osp.citations.hlom.jobs.query import query
from osp.citations.hlom import queries
from clint.textui.progress import bar
from scipy.stats import rankdata
from prettytable import PrettyTable
from rq import Queue


@click.group()
def cli():
    pass


@cli.command()
def init_db():

    """
    Create the database tables.
    """

    pg_local.connect()
    pg_remote.connect()

    pg_local.create_tables([
        HLOM_Record
    ], safe=True)

    pg_remote.create_tables([
        HLOM_Citation
    ], safe=True)


@cli.command()
@click.option('--n', default=10000)
def insert_records(n):

    """
    Write the records into the database.
    """

    dataset = Dataset.from_env()

    i = 0
    for group in dataset.grouped_records(n):

        rows = []
        for record in group:

            # Just records with title/author.
            if record and record.title() and record.author():
                rows.append({
                    'control_number': record['001'].format_field(),
                    'record': record.as_marc()
                })

        if rows:
            HLOM_Record.insert_many(rows).execute()

        i += 1
        sys.stdout.write('\r'+str(i*n))
        sys.stdout.flush()


@cli.command()
def queue_queries():

    """
    Queue citation extraction queries.
    """

    queue = Queue(connection=redis)

    for record in HLOM_Record.select().naive().iterator():
        queue.enqueue(query, record.id)


@cli.command()
@click.argument('out_path', type=click.Path())
def csv_text_counts(out_path):

    """
    Write a CSV with text -> assignment count.
    """

    out_file = open(out_path, 'w')

    # CSV writer.
    cols = ['title', 'author', 'count', 'subjects']
    writer = csv.DictWriter(out_file, cols)
    writer.writeheader()

    rows = []
    for c in queries.text_counts().naive().iterator():

        row = HLOM_Record.get(
            HLOM_Record.control_number==c.record
        )

        # Gather subject field values.
        subjects = [s.format_field() for s in row.pymarc.subjects()]

        rows.append({
            'title': row.pymarc.title(),
            'author': row.pymarc.author(),
            'count': c.count,
            'subjects': ','.join(subjects)
        })

    writer.writerows(rows)


@cli.command()
@click.argument('out_path', type=click.Path())
def csv_syllabus_counts(out_path):

    """
    Write a CSV with syllabus -> citation count.
    """

    out_file = open(out_path, 'w')

    # CSV writer.
    cols = ['document', 'count']
    writer = csv.DictWriter(out_file, cols)
    writer.writeheader()

    rows = []
    for c in queries.syllabus_counts().naive().iterator():

        rows.append({
            'document': c.document,
            'count': c.count
        })

    writer.writerows(rows)


@cli.command()
@click.option('--page_len', default=1000)
def push_objects(page_len):

    """
    Write HLOM records as store objects in Overview.
    """

    ov = Overview.from_env()

    # Wrap the query in a progress bar.
    query = query_bar(queries.records_with_citations())

    for group in grouper(query, page_len):

        objects = []
        for r in group:
            objects.append({
                'indexedLong': r.id,
                'indexedString': None,
                'json': {}
            })

        ov.post_object(objects)


@cli.command()
def pull_overview_ids():

    """
    Copy store object ids from Overview.
    """

    ov = Overview.from_env()
    objects = ov.list_objects().json()
    size = ov.count_objects()

    for obj in bar(objects, expected_size=size):

        query = (
            HLOM_Record
            .update(stored_id=obj['id'])
            .where(HLOM_Record.id==obj['indexedLong'])
        )

        query.execute()


@cli.command()
@click.option('--page_len', default=1000)
def push_document_objects(page_len):

    """
    Write HLOM citations as document -> store objects in Overview.
    """

    ov = Overview.from_env()

    # Wrap the query in a progress bar.
    query = query_bar(queries.document_objects())

    for group in grouper(query, page_len):

        objects = []
        for d2r in group:
            objects.append([d2r.did, d2r.rid])

        ov.post_document_objects(objects)


@cli.command()
def write_citation_counts():

    """
    Cache a citation count value on the HLOM records.
    """

    query = query_bar(queries.text_counts())

    for pair in query:

        # Get a modified HSTORE value.
        updated = HLOM_Record.metadata.update(
            citation_count=str(pair.count)
        )

        # Update the HLOM record.
        query = (
            HLOM_Record
            .update(metadata=updated)
            .where(HLOM_Record.control_number==pair.record)
        )

        query.execute()


@cli.command()
def write_deduping_hash():

    """
    Cache a "deduping" hash on HLOM records.
    """

    query = query_bar(queries.records_with_citations())

    for record in query:

        # Get a modified HSTORE value.
        updated = HLOM_Record.metadata.update(
            deduping_hash=record.hash
        )

        # Update the HLOM record.
        query = (
            HLOM_Record
            .update(metadata=updated)
            .where(HLOM_Record.id==record.id)
        )

        query.execute()


@cli.command()
def write_teaching_rank():

    """
    Write a "teaching rank" score on HLOM records.
    """

    # Get a set of id -> count tuples.
    pairs = []
    for record in queries.deduped_records():
        pairs.append((
            record.id,
            record.metadata['citation_count'])
        )

    # Rank the counts.
    counts = [p[1] for p in pairs]
    ranks = rankdata(counts, 'max')

    # Rank ascending.
    ranks = ranks.max()+1 - ranks

    # Write the ranks.
    for i, rank in enumerate(bar(ranks)):

        id = pairs[i][0]

        # Get a modified HSTORE value.
        updated = HLOM_Record.metadata.update(
            teaching_rank=str(int(rank))
        )

        # Update the HLOM record.
        query = (
            HLOM_Record
            .update(metadata=updated)
            .where(HLOM_Record.id==id)
        )

        query.execute()
