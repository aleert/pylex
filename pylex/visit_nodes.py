import ast
from ast import NodeVisitor
from pathlib import Path
from typing import Iterable

import visitor_mixins

NODE_TYPES = {
    'FunctionDef': visitor_mixins.FunctionDefMixin,
    'function': visitor_mixins.FunctionDefMixin,
    'ClassDef': visitor_mixins.ClassDefMixin,
    'class': visitor_mixins.ClassDefMixin,
    'Assign': visitor_mixins.AssignMixin,
    'assign': visitor_mixins.AssignMixin,
}


def count_pt_of_speech_in_tree(
    tree_path: Path,
    node_types: Iterable,
    target_part='VB',
    exclude_dunder=True,
    exclude_private=False,
):
    """Return (Counter(matching_names), num_nodes_explored) tuple."""
    mixins = []
    for node_type in node_types:
        if node_type in NODE_TYPES.keys():
            mixins.append(NODE_TYPES[node_type])
    mixins.append(NodeVisitor)

    Visitor = type('Visitor', tuple(mixins), {})

    tree = ast.parse(tree_path.read_bytes())
    visitor = Visitor(target_part, exclude_dunder=exclude_dunder, exclude_private=exclude_private)
    visitor.visit(tree)
    return visitor.counter, visitor.nodes_explored
