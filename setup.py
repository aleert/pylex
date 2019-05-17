# -*- coding: utf-8 -*-
import importlib
from io import open

from setuptools import find_packages, setup
from setuptools.command.install import install


def read(f):
    return open(f, 'r', encoding='utf-8').read()


class PostInstallCommand(install):
    """Download averaged_perceptron_tagger for nltk."""

    def run(self):
        nltk = importlib.import_module('nltk')
        print(nltk)
        nltk.download('averaged_perceptron_tagger')
        install.run(self)


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
    ],
    extras_require={
        'dev': [
            'wemake-python-styleguide>=0.8.1',
        ],
    },
    cmdclass={
        'install': PostInstallCommand,
    },
    python_requires='>=3.4',
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
    ],
    entry_points={
        'console_scripts': [
            'pylex = pylex.cli:main',
        ],
    },
)
