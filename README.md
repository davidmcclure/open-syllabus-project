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

Everything is bundled up under a top-level `osp` executable. Run `osp`, and you should get the default help output:

```bash
Usage: osp [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  corpus
  institutions
  locations
```

## Usage

Everything is bunled under the o
