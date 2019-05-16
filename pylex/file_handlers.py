# -*- coding: utf-8 -*-

"""Utilities to find *.py files and explore their ASTs."""
import ast
import logging
from importlib import import_module
from pathlib import Path
from typing import Generator, List, Text, Tuple

from git import GitCommandError
from tqdm import tqdm

from pylex.git_handlers import download_git_repo


def get_py_from_module(module_or_path: str) -> Generator[Path, None, None]:  # noqa: C901
    """
    Generate all *.py files in module or path.

    Raises FileNotFoundError if specified module has no __file__ of __path__ set
    (some built-ins like math).
    Raises OSError if specified file or path doesn't exist or cant be accessed
    for other reasons (e.g. you you have no read permissions).
    """
    if module_or_path.endswith('.git'):
        try:
            cloned_path = download_git_repo(module_or_path)
            yield from cloned_path.glob('**/*.py')
            return
        except GitCommandError:
            raise OSError('Cannot clone repo \'{0}\''.format(module_or_path))

    try:
        module = import_module(module_or_path)

        # try to guess file location
        if hasattr(module, '__path__') and module.__path__[0]:
            path = Path(module.__path__[0])
        elif hasattr(module, '__file__') and module.__file__.endswith('__init__.py'):
            path = Path(module.__file__).parent
        elif hasattr(module, '__file__'):
            path = Path(module.__file__)
        else:
            raise FileNotFoundError('Can\'t find files for module {0}.'.format(module))
    except (ImportError, TypeError):
        path = Path(module_or_path)

    # just a *.py file
    if path.suffix == '.py' and path.exists():
        yield path
        return
    elif path.is_dir() and path.exists():
        yield from path.glob('**/*.py')
        return

    # it must be github account/repo pair then..
    elif len(path.parts) == 2:
        path = 'https://github.com/' + '/'.join(path.parts) + '.git'
        try:
            cloned_path = download_git_repo(path)
            yield from cloned_path.glob('**/*.py')
            return
        except GitCommandError:
            raise OSError('Cannot clone repo \'{0}\''.format(path))

    raise OSError('Cannot resolve \'{0}\''.format(path))


def get_all_py(modules: List[Text], write_log: bool = False) -> Generator[Path, None, None]:
    """Generate *py files from many modules or paths."""
    for module in modules:
        if write_log:
            logging.info('Processing {0}'.format(module))
            yield from tqdm(get_py_from_module(module), unit=' files', desc='Parsing')
        else:
            yield from get_py_from_module(module)


def tree_from_py_file_path(pyfile: Path) -> Tuple[ast.Module, str]:
    """Return tree with filename given Path to *.py file."""
    try:
        tree = ast.parse(pyfile.read_bytes())
        return tree, str(pyfile)
    except SyntaxError:
        logging.error('cannot parse {0}'.format(pyfile))
        return ast.Module(), ''
