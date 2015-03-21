
# OSP Workflow

## Extract text from OSP documents

1. `osp corpus init_db` - Create the document / metadata tables.

1. `osp corpus insert_documents` - Create a row in `document` for each OSP syllabus.

1. `osp queue_read_text` (local) / `osp workers queue_text` (EC2) - Queue text-extraction jobs, which write rows into `document_text`.

1. `osp queue_read_format` - Queue format-extraction jobs.

## Index OSP documents in Elasticsearch

1. `osp corpus_index create` - Create the ES index, set the mapping.

1. `osp corpus_index insert` - Bulk-index documents in Elasticsearch.

## Extract citations

1. `osp hlom init_db` - Create the HLOM record / metadata tables.

1. `osp hlom insert_records` - Create a row in `hlom_record` for each MARC record.

**TODO**: Why doesn't this work on Ubuntu?

1. `osp hlom queue_queries` (local) / `osp workers queue_hlom` (EC2) - Queue citation-extraction queries, which write rows into `hlom_citation`.

## Index HLOM records in Elasticsearch

1. `osp hlom_index create` - Create the ES index, set the mapping.

1. `osp hlom write_citation_counts` - Denormalize the citation counts for each record.

1. `osp hlom write_blacklist [PATH]` - Exclude manually-identified nonsense records, where `PATH` is a .txt file with a list of MARC control numbers.

1. `osp write_deduping_hash` - Write a hash onto each record that (in theory) collapses together the unique title/author combinations.

1. `osp write_metrics` - Write teaching rank / percentile metrics.

1. `osp hlom_index insert` - Insert the HLOM documents.

## Geocode institutions

1. `osp institutions init_db` - Create the institution / metadata tables.

1. `osp institutions insert data/institutions.csv` - Create a row in `institution` for each listing in the CSV of US-accredited institutions.

1. `osp institutions queue_geocoding` - Queue geocoding jobs, which write rows to `institution_lonlat`.

**TODO**: Find a replacement for the MapQuest geocoder?

## Match documents with syllabi

1. `osp locations init_db` - Create the `document_institution` mapping table.

1. `osp locations queue_matching` (local) / `osp workers queue_locate` (EC2) - Queue document -> institution matching jobs, which write rows to `document_institution`.
