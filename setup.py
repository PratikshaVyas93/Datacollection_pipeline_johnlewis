from setuptools import setup
from setuptools import find_packages

setup(
    name='johnlewis_web_scraper',
    version='0.0.1',
    description='Package allows you to scrape data about the mobile products on johnlewis.com',
    url='https://github.com/PratikshaVyas93/Datacollection_pipeline_johnlewis',
    author='Pratiksha',
    license='MIT',
    packages=find_packages(),
    install_requires=['pandas', 'selenium','sqlalchemy','boto3','psycopg2-binary'],
)
