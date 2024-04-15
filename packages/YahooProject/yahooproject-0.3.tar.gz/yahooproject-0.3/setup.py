from setuptools import setup, find_packages

setup(
    name='YahooProject',
    version='0.3',
    packages=['YahooProject'],
    install_requires=[
        'requests',
        'beautifulsoup4'
    ],
    author='Nick37',
    description='A package for scraping search results from Yahoo Search.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)