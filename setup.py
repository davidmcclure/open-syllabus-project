

from setuptools import setup, find_packages


setup(

    name='osp',
    version='0.1.0',
    description='OSP file management and metadata extraction.',
    url='https://github.com/overview/osp',
    license='Apache',
    author='David McClure',
    author_email='davidwilliammcclure@gmail.com',
    packages=find_packages(),
    scripts=['bin/osp'],

    install_requires=[

        'ipython',
        'matplotlib',
        'jsonschema',
        'tldextract',
        'geopy',
        'redis',
        'rq',
        'rq-dashboard',
        'click',
        'psycopg2',
        'python-magic',
        'requests',
        'clint',
        'prettytable',
        'circus',
        'beautifulsoup4',
        'jsonstream',
        'ijson',
        'pypdf2',
        'elasticsearch',
        'blessings',
        'anyconfig',
        'PyYAML',
        'uwsgi',
        'flask',
        'boto',
        'numpy',
        'scipy',
        'reportlab',
        'python-docx',
        'pdfminer3k',
        'pytest',
        'spacy',

        # Forks, via GitHub.
        'pymarc',
        'peewee',

    ]

)
