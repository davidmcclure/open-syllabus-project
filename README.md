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

Most of the commands don't have dependencies on other tasks, but there are a few cases where you need to do things in a sequence - for example, you'll need to load the institutions into the database before trying to match the document URLs to parent institutions. To get started:

### Geocode institutions

1. Run `osp institutions init_db` to install the `intitution` and `institution_lonlat` tables.

1. Run `osp institutions insert_institutions data/institutions.csv` to create a database row for each accredited institution.

1. With Redis running, run `osp queue_geocoding`. This queues up a request to the MapQuest geocoding API for each institution, managed by the RQ job queue library.

1. Open up a new terminal tab, run `rq-dashboard`, and hit `http://0.0.0.0:9181` in a browser.
