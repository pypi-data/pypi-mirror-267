from setuptools import setup, find_packages

setup(
    name='wansuite',
    version='8.0',
    description='A Simplified Toolkits  ',
    packages=find_packages(include=['wansuite','marketdata','macrodata','media','order','strategy']),
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


