# -*- coding: utf-8 -*-
from io import open

from setuptools import find_packages, setup


def read(f):
    return open(f, 'r', encoding='utf-8').read()


setup(
    name='pylex',
    version=0.1,
    license='BSD',
    description='Small CLI tool for lexical analysis of python code.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='Aleksei Panfilov',
    author_email='aleert@yandex.ru',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=[
        'nltk>=3.3',
        'appdirs>=1.4',
        'gitpython==2.1.8',
        'tqdm>=4.32',

    ],
    extras_require={
        'dev': [
            'wemake-python-styleguide>=0.8.1',
        ],
    },
    python_requires='>=3.6',
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
    ],
    entry_points={
        'console_scripts': [
            'pylex = pylex.cli:main',
        ],
    },
)
