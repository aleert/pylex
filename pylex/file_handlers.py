# -*- coding: utf-8 -*-

"""Utilities to find *.py files and explore their ASTs."""
import ast
from collections import Counter
from importlib import import_module
from pathlib import Path
from typing import Generator, List, Text, Tuple

import nltk

accepted_node_types = {
    'FunctionDef': ast.FunctionDef,
    'ClassDef': ast.ClassDef,
    'AsyncFunctionDef': ast.AsyncFunctionDef,
    'alias': ast.alias,
    'ExceptHandler': ast.ExceptHandler,
}


# looks like we have to deal with Jones complexity 8 here
def get_py_from_module(module_or_path: str) -> Generator[Path, None, None]:  # noqa: C901
    """
    Generate all *.py files in module or path.

    Raises FileNotFoundError if specified module has no __file__ of __path__ set
    (some built-ins like math).
    Raises OSError if specified file or path doesn't exist or cant be accessed
    for other reasons (e.g. you you have no read permissions).
    """
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
            raise FileNotFoundError('Can\'t find {0} files location.'.format(module))
    except (ImportError, TypeError):
        path = Path(module_or_path)

    # just a *.py file
    if path.suffix == '.py' and path.exists():
        yield path
        return
    elif path.is_dir() and path.exists():
        yield from path.glob('**/*.py')
        return

    raise OSError('Cannot open path \'{0}\''.format(path))


def get_all_py(modules: List[Text]) -> Generator[Path, None, None]:
    """Generate *py files from many modules or paths."""
    for module in modules:
        yield from get_py_from_module(module)


def tree_from_py_file_path(pyfile: Path) -> Tuple[ast.Module, str]:
    """Return tree with filename given path to *.py file."""
    try:
        tree = ast.parse(pyfile.read_bytes())
        return tree, str(pyfile)
    except SyntaxError:
        raise SyntaxError('cannot parse {0}'.format(pyfile))


def gen_node_names_from_tree(
    node_type: Text,
    tree: ast.Module,
    exclude_dunder: bool = True,
) -> Generator[str, None, None]:
    """
    Generate all `node_type` (name, nodes_inspected_so_far) tuples from tree.

    If `exclude_dunder` any dunder names wont be counted.

    `node_type` has to have `name` field.
    As of python3.7 those are (AsyncFunctionDef, FunctionDef, ClassDef, alias and ExceptHandler.
    """
    nd_type = accepted_node_types.get(node_type, '')
    if not nd_type:
        raise KeyError('Wrong node type {0}, select one from {1}'.format(
            node_type, accepted_node_types.keys(),
        ),
        )

    for node in ast.walk(tree):
        if isinstance(node, nd_type):
            if exclude_dunder and node.name.startswith('__') and node.name.endswith('__'):
                continue
            yield node.name


def is_part_of_speech(word: str, target_part: str = 'VB') -> bool:
    """Check if `word` is of `target_type` type of speech."""
    if not word:
        return False
    # consider using post_tag(tagset='universal')
    pos_info = nltk.pos_tag([word])
    return pos_info[0][1] == target_part


def split_name(name: str) -> Generator[str, None, None]:
    """Split name to tokens by underscore."""
    yield from iter(name.split('_'))


def count_pt_of_speech_in_tree(
    tree: ast.Module,
    node_type: str,
    target_part: str = 'VB',
) -> Tuple[Counter, int]:
    """Return (Counter(matching_names), num_nodes_explored) tuple."""
    nodes_explored = 0
    matching_counter = Counter()
    for node_num, node_name in enumerate(gen_node_names_from_tree(node_type, tree)):
        for name in split_name(node_name):
            if is_part_of_speech(name, target_part):
                matching_counter.update([name])
        nodes_explored = node_num + 1
    return matching_counter, nodes_explored
