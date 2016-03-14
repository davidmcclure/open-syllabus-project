
# OSP data

The data behind the Open Syllabus Project consists of two main parts:

- The raw corpus of ~1.5M syllabi and the original bibliographic databases (JSTOR, Harvard Library Cloud, CiteSeer), stored on EBS volumes that can get mounted to EC2 instances.

- A Postgres database, populated by this codebase. This database contains representations of various entities in the original corpora (syllabi, texts, institutions) so they can be easily linked with other relational data. It also stores the raw results of the routines that extract text assignments and link the syllabi with fields, institutions, and locations.

## Schema

The extraction database includes these tables:

- **`document`** (~1.4M rows) - A simple database representation of each syllabus in the OSP corpus. This table just contains a `path` column that points back to the location of the original document (relative to the corpus root).

- **`text`** (~15.3M rows) - Bibliographic records for the set of texts that OSP searches for in the syllabi. These are currently pulled from the [Harvard Library Open Metadata](http://library.harvard.edu/open-metadata) MARC records and the JSTOR catalog.

  There are two boolean flags on this table that are important from an analytical perspective. The `valid` flag contains the result of a data-cleaning process that decides whether or not the citation matches for a given text should be considered valid. This is based on the probability that the words in the author surname and title would appear together at random, based on frequencies of the words in large modern corpora.

  Second, the `display` flag is the result of a deduping process that tries to coalesce different versions of the same text. Eg, if there are 20 editions of "Republic, Plato" - one of them will have `display=true`, and all the rest will have `display=false`.

  Generally, when querying against this table - take texts for which both `valid` and `display` are true. (This is baked into APIs used to index the public-facing interface - eg, the `Text_Index.rank_texts()` method.)

- **`citation`** (~27M rows) - The raw results of the citation extraction job. Each row represents an individual text assignment - a link between a `document` and a `text`. This table is big, but a large majority of the rows are actually false-positives that get produced by a minority of texts that have extremely common words in both the author and title fields. These can be filtered out by joining on the text table and filtering out texts with `valid=false`, which produces a set of ~5M "good" citations.
