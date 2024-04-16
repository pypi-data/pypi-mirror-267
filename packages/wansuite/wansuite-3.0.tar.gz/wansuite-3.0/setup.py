from setuptools import setup, find_packages

setup(
    name='wansuite',
    version='3.0',
    description='A Simplified Toolkits for Wan ',
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


