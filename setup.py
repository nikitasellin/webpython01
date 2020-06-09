import os

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='webpython-hw01',
    version='0.1',
    packages=['webpython_hw01', ],
    include_package_data=True,
    license='GNU General Public License v3.0',
    description='Google/Yahoo console searcher.',
    long_description=README,
    url='https://github.com/nikitasellin/webpython01',
    author='Nikita A. Selin',
    author_email='nikita@selin.com.ru',
    keywords=['console', 'searcher', 'google', 'yahoo'],
    python_requires='==3.8.3',
    install_requires=[
         "beautifulsoup4==4.9.0",
    ],
    entry_points={
        'console_scripts': [
            'searcher = webpython_hw01.searcher:main',
        ]
    },
)
