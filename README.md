# Open Syllabus Project

This repository contains a collection of packages and command line utilities for interacting with the OSP corpus, extracting metadata, and loading data into Overview.

Read about the **[Open Syllabus Project](http://opensyllabusproject.org)**.

## Installation

The easiest way to get started is to install the package in `develop` mode:

1. Clone the repo, change into it, and create a Python virtual environment with `pyvenv env`.

1. Activate the environment with `. env/bin/activate`.

1. Install the dependencies with `pip3 install -r requirements.txt`.

1. Install the package with `python setup.py develop`.

1. Create a local Postgres database with `createdb osp`. This database is used as a holding ground to store metadata before it gets pushed into Overview.

1. Install the `hstore` extension on the database with `psql osp`, `CREATE EXTENSION hstore;`.

1. Set a `OSP_CORPUS` env variable with a local path to the OSP corpus.

Run `osp`, and you should get the default help output:

```bash
> osp

Usage: osp [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  corpus
  institutions
  locations
```

## Usage

The actual functionality is exposed through subcommands under `osp`. For example, `osp corpus` provides summary statistics about the corpus and file management helpers:

```bash
> osp corpus

Usage: osp corpus [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  file_count         Print the total number of files.
  file_type_counts   Print a list of file type -> count.
  init_db            Create the database tables.
  insert_documents   Insert documents in the database.
  pull_overview_ids  Copy document ids from Overview.
```

Most of the commands don't have dependencies on other tasks, but there are a few cases where you need to do things in a sequence - for example, you'll need to load the institutions into the database before trying to match the document URLs to parent institutions.

### Geocode institutions

First, let's get coordinates for each US-accredited institution.

1. Run `osp institutions init_db` to install the `intitution` and `institution_lonlat` tables.

1. Set a `MAPQUEST_KEY` environment variable with a MapQuest API key.

1. Run `osp institutions insert_institutions data/institutions.csv` to create a database row for each accredited institution.

1. With Redis running, run `osp institutions queue_geocoding`. This queues up a request to the MapQuest geocoding API for each institution, managed by the [RQ](http://python-rq.org) job queue library.

1. Open up a new terminal tab, reactivate the Python virtual environment we created for the project, and run `rq-dashboard`, and hit `http://0.0.0.0:9181` in a browser.

1. Open up another tab, and run `rqworker` to start a single queue worker, which will start processing the geocoding jobs immediately. You'll probably want to start 7-8 of these.

### Match documents with institutons

Next, we need to match each document in the corpus with with an institution.

1. Run `osp locations init_db` to install the document -> institution table.

1. Run `osp locations queue_location_matching` to queue up the workers. If they're not already running, start some `rqworker` processes to do the work, like before.

### Push institutions into Overview as store objects

The next couple steps assume that you've uploaded some OSP documents to a collection in Overview. (The documents in Overview don't have to one-to-one match the files in the corpus, so it's fine to just upload a small subset for testing). Once you've got a document collection, add env variables for `OSP_API_URL`, `OSP_API_TOKEN`, and `OSP_DOC_SET_ID`. So, in total:

```
export OSP_CORPUS=/path/to/corpus
export OSP_API_URL=http://localhost:9000/api/v1
export OSP_API_TOKEN=XXXX
export OSP_DOC_SET_ID=X
```

Now, we can write the institutions into Overview as store objects:

1. Run `osp institutions write_store_objects` to write the objects.

1. Then, run `osp institutions pull_overview_ids` to write the Overview-generated object ids back into the local extraction database.

### Pull Overview document ids

Next, we need to do the same thing for documents - map the unique names of the files in the corpus with the Overview ids.

1. Run `osp corpus init_db` to install the documents table.

1. Run `osp corpus insert_documents` to register a row for each document.

1. Last, run `osp corpus pull_overview_ids` to, you guessed it, pull in the ids.

### Push document -> institution links as document objects

1. Just run `osp locations write_document_objects`.
