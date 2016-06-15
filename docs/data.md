
# OSP data

The data behind the Open Syllabus Project consists of two main parts:

- The raw corpus of ~1.5M syllabi and the original bibliographic databases (JSTOR, Harvard Library Cloud, CiteSeer), stored on EBS volumes that can get mounted to EC2 instances.

- A Postgres database, populated by this codebase. This database contains representations of various entities in the original corpora (syllabi, texts, institutions) so they can be easily linked with other relational data. It also stores the raw results of the routines that extract text assignments and link the syllabi with fields, institutions, and locations.



# Schema

The extraction database includes the following tables:

document
--------
(~1.4M rows) - A simple database representation of each syllabus in the OSP corpus. This table just contains a `path` column that points back to the location of the original document (relative to the corpus root).

    osp=> \d+ document
                                                      Table "public.document"
      Column  |            Type             |                 Modifiers          | Storage  | Stats target | Description
    ----------+-----------------------------+------------------------------------+----------+--------------+-------------
     id       | integer                     | not null default next document_id  | plain    |              |
     created  | timestamp without time zone | not null                           | plain    |              |
     path     | character varying(255)      | not null                           | extended |              |
     metadata | jsonb                       | not null                           | extended |              |


Sample data:

    osp=> select * from document LIMIT 3 OFFSET 400;
    -[ RECORD 1 ]-------------------------------
    id       | 401
    created  | 2015-12-21 23:39:16.459392
    path     | 001/25d559a1a29f73b0c790b66ee5266
    metadata | {}
    -[ RECORD 2 ]-------------------------------
    ...

This is the main lookup table between the `id` field used in the DB and the path
of the original document in the corpus.


text
----
(~15.3M rows) - Bibliographic records for the set of texts that OSP searches for in the syllabi. These are currently pulled from the [Harvard Library Open Metadata](http://library.harvard.edu/open-metadata) MARC records and the JSTOR catalog.

Sample data:

    -[ RECORD 1 ]------+--------------------------------------------------------
    id                 | 400
    created            | 2016-01-02 06:30:46.088968
    corpus             | hlom
    identifier         | 005000471-9
    url                |
    title              | Coutumes algeriennes.
    surname            | Maunier
    authors            | {"Maunier, René, 1887-"}
    publisher          | Domat-Montchrestien,
    date               | 1935.
    journal_title      |
    journal_identifier |
    issue_volume       |
    issue_number       |
    issue_chronology   |
    pagination         |
    valid              |
    display            |
    -[ RECORD 2 ]------+--------------------------------------------------------
    id                 | 401
    created            | 2016-01-02 06:30:46.089729
    corpus             | hlom
    identifier         | 005000472-7
    url                |
    title              | Catalogue of the Germanic Museum exhibition of German paintings of the fifteenth and sixteenth centuries : lent from American collections ; Harvard University tercentenary celebration, June 5 to September 30, 1936.
    surname            | Harvard University. Germanic Museum.
    authors            | {"Harvard University. Germanic Museum."}
    publisher          | The Museum,
    date               | 1936].
    journal_title      |
    journal_identifier |
    issue_volume       |
    issue_number       |
    issue_chronology   |
    pagination         |
    valid              |
    display            |

There are two boolean flags on this table that are important from an analytical perspective. The `valid` flag contains the result of a data-cleaning process that decides whether or not the citation matches for a given text should be considered valid. This is based on the probability that the words in the author surname and title would appear together at random, based on frequencies of the words in large modern corpora.

Second, the `display` flag is the result of a deduping process that tries to coalesce different versions of the same text. Eg, if there are 20 editions of "Republic, Plato" - one of them will have `display=true`, and all the rest will have `display=false`.

Generally, when querying against this table - take texts for which both `valid` and `display` are true. (This is baked into APIs used to index the public-facing interface - eg, the `Text_Index.rank_texts()` method.)

citation
--------
(~27M rows) - The raw results of the citation extraction job. Each row represents an individual text assignment - a link between a `document` and a `text`. This table is big, but a large majority of the rows are actually false-positives that get produced by a minority of texts that have extremely common words in both the author and title fields. These can be filtered out by joining on the text table and filtering out texts with `valid=false`, which produces a set of ~5M "good" citations.

    osp=> \d citation;
                                          Table "public.citation"
       Column    |            Type             |                       Modifiers
    -------------+-----------------------------+-------------------------------------------------------
     id          | integer                     | not null default nextval('citation_id_seq'::regclass)
     created     | timestamp without time zone | not null
     text_id     | integer                     | not null
     document_id | integer                     | not null
     tokens      | character varying(255)[]    | not null

Sample data:

    osp=> select * from citation LIMIT 5 OFFSET 300;
      id  |          created           | text_id | document_id |                                         tokens
    ------+----------------------------+---------+-------------+----------------------------------------------------------------------------------------
      301 | 2016-01-17 17:42:37.869801 | 1809855 |      816945 | {blodgett,grasp,tight,old,ways,selections,from,klamer,family,collection,of,inuit,art}
      302 | 2016-01-17 17:42:37.869822 | 1809855 |       85853 | {blodgett,grasp,tight,old,ways,selections,from,klamer,family,collection,of,inuit,art}
      303 | 2016-01-17 17:42:38.542057 | 5429302 |      669183 | {pollard,genesis,of,modern,management,study,of,industrial,revolution,in,great,britain}
      304 | 2016-01-17 17:42:38.542137 | 5429302 |     1411776 | {pollard,genesis,of,modern,management,study,of,industrial,revolution,in,great,britain}
     2582 | 2016-01-17 17:43:29.266326 | 5429485 |      550743 | {smith,foods}



institution
-----------
(~12k rows) - A set of institutions, loaded from public datasets included in the `institutions` module.

                                                            Table "public.institution"
     Column  |            Type             |                        Modifiers                         | Storage  |
    ---------+-----------------------------+----------------------------------------------------------+----------+
     id      | integer                     | not null default nextval('institution_id_seq'::regclass) | plain    |
     created | timestamp without time zone | not null                                                 | plain    |
     name    | character varying(255)      | not null                                                 | extended |
     url     | character varying(255)      | not null                                                 | extended |
     domain  | character varying(255)      | not null                                                 | extended |
     state   | character varying(255)      |                                                          | extended |
     country | character varying(255)      | not null                                                 | extended |

Sample data:

    select * from institution LIMIT 3 OFFSET 20;
    -[ RECORD 1 ]----------------------------------
    ...
    -[ RECORD 2 ]----------------------------------
    id      | 12196
    created | 2015-12-29 23:33:08.243834
    name    | Kazak State University of Agriculture
    url     | http://www.agriun.almaty.kz/
    domain  | almaty.kz
    state   |
    country | KZ
    -[ RECORD 3 ]----------------------------------
    ...


institution_document
--------------------
(~1M rows) - The results of the `syllabus -> institution` matching routine. Each row links a document and an institution.

    osp=> select * from institution_document LIMIT 3 OFFSET 20;
    -[ RECORD 1 ]--+---------------------------
    id             | 21
    created        | 2015-12-29 23:37:35.708702
    institution_id | 1601
    document_id    | 569613
    -[ RECORD 2 ]--+---------------------------
    id             | 22
    created        | 2015-12-29 23:37:35.716954
    institution_id | 5908
    document_id    | 569615
    -[ RECORD 3 ]--+---------------------------
    id             | 23
    created        | 2015-12-29 23:37:35.725973
    institution_id | 1817
    document_id    | 569616


document_text
-------------
(~1.4M rows) The plain text extracted from the documents. For copyright / privacy reasons, this table is excluded from the public data dump.


                                                              Table "public.document_text"
       Column    |            Type             |                         Modifiers                          | Storage  |
    -------------+-----------------------------+------------------------------------------------------------+----------+
     id          | integer                     | not null default nextval('document_text_id_seq'::regclass) | plain    |
     created     | timestamp without time zone | not null                                                   | plain    |
     document_id | integer                     | not null                                                   | plain    |
     text        | text                        | not null                                                   | extended |

Sample data:

    osp=> select * from document_text LIMIT 1 OFFSET 20001;
    -[ RECORD 1 ]------------------------------------------------------------------------------------------------
    id          | 19922
    created     | 2015-12-28 19:29:03.655269
    document_id | 709354
    text        | Minor in Technical And Professional Writing                                                   +
                |       This interdisciplinary minor is for students who have a desire to pursue                +
                |       a career in writing and/or to focus on writing in their careers and within              +
                |       their disciplines. It consists of 18 semester hours, which includes four                +
                |       ...





Fields, subfields, and classification
-------------------------------------

- **`field`** (49 rows) - A collection of top-level fields, as defined by our [work-in-progress spreadsheet](https://docs.google.com/spreadsheets/d/1USyxe1qD1zi-Cv0_xUkrjcGSYKz5-vefJ58KbL8iiQQ/edit?usp=sharing).

- **`subfield`** (261 rows) - More granular fields, each linked to a parent `field` row.

- **`subfield_document`** (700k rows) - The results of the `syllabus -> fields` matching routine - each row links a syllabus with a field. This is done by looking for "course code" numbers like `MATH 101`, `HIST 400`, etc.


        osp=> select * from field LIMIT 2 OFFSET 10;
        -[ RECORD 1 ]-----------------------
        id      | 11
        created | 2015-12-30 16:50:31.189755
        name    | Classics
        -[ RECORD 2 ]-----------------------
        id      | 12
        created | 2015-12-30 16:50:31.215998
        name    | Computer Science
        
        osp=> select * from subfield LIMIT 2 OFFSET 10;
        -[ RECORD 1 ]-+---------------------------
        id            | 11
        created       | 2015-12-30 16:50:30.768155
        name          | Anthropology
        abbreviations | {ANTH}
        field_id      | 2
        -[ RECORD 2 ]-+---------------------------
        id            | 12
        created       | 2015-12-30 16:50:30.772953
        name          | Archeology
        abbreviations | {ARCHAE}
        field_id      | 2
        
        osp=> select * from subfield_document LIMIT 2 OFFSET 10;
        -[ RECORD 1 ]-----------------------------------------------------------------------
        id          | 11
        created     | 2015-12-30 17:28:35.316288
        subfield_id | 148
        document_id | 283005
        offset      | 17192
        snippet     |  math. Passing the assessment is a prerequisite for enrollment...
        -[ RECORD 2 ]-----------------------------------------------------------------------
        id          | 12
        created     | 2015-12-30 17:28:35.35368
        subfield_id | 63
        document_id | 424505
        offset      | 65
        snippet     | MGRS 308 (492) Salesmanship and Negotiation for CRM Page 1 of 3 MKT ...




