from setuptools import setup, find_packages

setup(
    name='wansuite',
    version='6.0',
    description='A Simplified Toolkits  ',
    packages=find_packages(),
    install_requires=[
       'yfinance',
'beautifulsoup4',
        'helium',
'mysql-connector-python',
'SQLAlchemy',
        'ib_insync',
        'nltk',
        'gensim',
        'nltk-downloader',
        'top2vec'



    ]
)


