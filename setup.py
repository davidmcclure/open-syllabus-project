

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
        'tldextract',
        'geopy',
        'redis',
        'rq',
        'rq-dashboard',
        'click',
        'psycopg2',
        'peewee',
        'python-magic',
        'requests',
        'clint',
        'prettytable',
        'circus',
        'beautifulsoup4',
        'jsonstream',
        'pypdf2',
        'elasticsearch',
        'blessings',
        'ijson',
        'anyconfig',
        'PyYAML',
        'uwsgi',
        'pymarc',
        'boto',
        'flask',
    ]

)
