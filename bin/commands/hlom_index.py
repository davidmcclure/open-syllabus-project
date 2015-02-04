

import math
import click
import re

from osp.common.models.base import elasticsearch as es
from osp.citations.hlom.dataset import Dataset
from osp.citations.hlom.models.record import HLOM_Record
from elasticsearch.helpers import bulk
from pymarc import Record
from clint.textui.progress import bar
from blessings import Terminal


@click.group()
def cli():
    pass


@cli.command()
def create():

    """
    Create the index.
    """

    es.indices.create('hlom', {
        'mappings': {
            'record': {
                '_id': {
                    'index': 'not_analyzed',
                    'store': True
                },
                'properties': {
                    'title': {
                        'type': 'string'
                    },
                    'author': {
                        'type': 'string'
                    },
                    'publisher': {
                        'type': 'string'
                    },
                    'pubyear': {
                        'type': 'integer'
                    },
                    'lists': {
                        'properties': {
                            'subjects': {
                                'type': 'string'
                            },
                            'notes': {
                                'type': 'string'
                            }
                        }
                    }
                }
            }
        }
    })


@cli.command()
def delete():

    """
    Delete the index.
    """

    es.indices.delete('hlom')


@cli.command()
@click.option('--page', default=10000)
def insert(page):

    """
    Index documents.
    """

    query = HLOM_Record.select()
    pages = math.ceil(query.count()/page)

    for p in bar(range(1, pages+1)):

        # Paginate the base query.
        paginated = query.paginate(p, page).iterator()

        docs = []
        for row in paginated:

            # Hydrate a MARC record.
            marc = Record(
                data=bytes(row.record),
                ascii_handling='ignore',
                utf8_handling='ignore'
            )

            # Get raw subject/notes values.
            subjects = [s.format_field() for s in marc.subjects()]
            notes = [n.format_field() for n in marc.notes()]

            # Try to get the pubyear as an int.
            pubyear = marc.pubyear()
            if pubyear:
                digits = re.search('\d+', marc.pubyear())
                if digits:
                    pubyear = int(digits.group(0))

            docs.append({
                '_id': row.control_number,
                'title': marc.title(),
                'author': marc.author(),
                'publisher': marc.publisher(),
                'pubyear': pubyear,
                'subjects': subjects,
                'notes': notes
            })

        # Bulk-index the page.
        bulk(es, docs, index='hlom', doc_type='record')


@cli.command()
@click.argument('q')
@click.option('--size', default=10)
@click.option('--start', default=0)
@click.option('--slop', default=10)
def search(q, size, start, slop):

    """
    Search records.
    """

    results = es.search('hlom', 'record', {
        'size': size,
        'from': start,
        'fields': [],
        'query': {
            'query_string': {
                'query': q
            }
        },
        'highlight': {
            'pre_tags': ['\033[1m'],
            'post_tags': ['\033[0m'],
            'fields': {
                'title': {}
            }
        }
    })

    term = Terminal()

    # Total hits.
    hits = str(results['hits']['total'])+' docs'
    click.echo(term.standout_cyan(hits))

    # Hit highlights.
    for hit in results['hits']['hits']:

        if 'highlight' in hit:
            click.echo('\n'+term.underline(hit['_id']))
            for snippets in hit['highlight'].values():
                for snippet in snippets:
                    click.echo(snippet)
