# -*- coding: utf-8 -*-

"""Mixins for ast.NodeVisitor for different types of nodes."""
from collections import Counter

import nltk
from typing import Text


def is_part_of_speech(word: Text, target_part: Text = 'VB') -> bool:
    """Check if `word` is of `target_type` type of speech."""
    if not word:
        return False
    # consider using post_tag(tagset='universal')
    pos_info = nltk.pos_tag([word])
    return pos_info[0][1] == target_part


def split_name(name):
    yield from iter(name.split('_'))


def is_dunder(name):
    if name.startswith('__') and name.endswith('__'):
        return True
    return False


def is_private(name):
    if name.startswith('_'):
        return True
    return False


class BaseMixin:
    """Implement convinient methods."""

    def __init__(self, pt_of_speech, exclude_dunder=True, exclude_private=True):
        self.pt_of_speech = pt_of_speech
        self.counter = Counter()
        self.exclude_dunder = exclude_dunder
        self.exclude_private = exclude_private
        self.nodes_explored = 0

    def skip_name(self, name):
        if self.exclude_private and is_private(name):
            return True
        if self.exclude_dunder and is_dunder(name):
            return True
        return False


class ClassDefMixin(BaseMixin):

    def visit_ClassDef(self, node):
        if self.skip_name(node.name):
            return self.generic_visit(node)
        for name_chunk in split_name(node.name):
            if is_part_of_speech(name_chunk, self.pt_of_speech):
                self.counter.update([name_chunk])
        self.nodes_explored += 1
        return self.generic_visit(node)


class FunctionDefMixin(BaseMixin):

    def visit_FunctionDef(self, node):
        if self.skip_name(node.name):
            return self.generic_visit(node)
        for name_chunk in split_name(node.name):
            if is_part_of_speech(name_chunk, self.pt_of_speech):
                self.counter.update([name_chunk])
        self.nodes_explored += 1
        return self.generic_visit(node)


class AssignMixin(BaseMixin):

    def visit_Assign(self, node):
        for name in node.targets:
            if self.skip_name(name):
                return self.generic_visit(node)
            for name_chunk in split_name(name):
                if is_part_of_speech(name_chunk, self.pt_of_speech):
                    self.counter.update([name_chunk])
        self.nodes_explored += 1
        return self.generic_visit(node)


