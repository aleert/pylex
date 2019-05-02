# -*- coding: utf-8 -*-

"""CLI interace."""
import collections
from typing import Counter, Dict, NewType, Tuple

import cleo

from pylex.file_handlers import count_pt_of_speech_in_tree, get_all_py, tree_from_py_file_path


class CountPartsOfSpeechCommand(cleo.Command):
    """
    Count parts of speech in python modules or files.

    count
        {name* : Packages or paths you want to explore.}
        {--top= : Print only top most common words. }
        {--P|pt-of-speech= : Part of speech as of nltk.help.upenn_tagset() (NN for noun,
                        VB for verb, CD for cardinal etc.) }
        {--N|node-type= : Node type to explore. FunctionDef, AsyncFunctionDef and ClassDef
                     are currently accepted. }
        {--S|split : Generate output for every file explored. }
    """

    help = """Count parts of speech you specify in packages.
              If no pt_of_speech provided, verb (VB) is used."""

    def handle(self):
        """Our main handler."""
        packages = self.argument('name')
        num_top = self.option('top') or 5
        num_top = int(num_top)
        pt_of_speech = self.option('pt-of-speech') or 'VB'
        node_type = self.option('node-type') or 'FunctionDef'

        # for type hinting
        FileName = NewType('Name', str)  # noqa: N806
        NodeNameCounter = NewType('NodeNameCounter', Counter[str])  # noqa: N806
        TotalNodeNamesCount = NewType('TotalNodeNamesCount', int)  # noqa: N806

        all_files = {}  # type: Dict[FileName, Tuple[NodeNameCounter, TotalNodeNamesCount]]

        try:
            for filepath in get_all_py(packages):
                tree, filename = tree_from_py_file_path(filepath)

                all_files[filename] = count_pt_of_speech_in_tree(
                    tree,
                    target_part=pt_of_speech,
                    node_type=node_type,
                )
        except OSError as error:
            self.line('<error>' + str(error) + '</error>')

        if self.option('split'):
            for filename, (cntr, node_count) in all_files.items():  # noqa: Z460, Z446
                self.line('<info>{0} nodes explored in file {1}</info>'.format(
                    node_count,
                    filename,
                ))
                self.line('Top {0} names are:'.format(num_top))
                for name, counts in cntr.most_common(num_top):
                    self.line('{0} : {1}'.format(name, counts))

        else:
            total_counts = collections.Counter()
            nodes_explored = 0
            files_explored = 0
            for _filename, (cntr, node_count) in all_files.items():  # noqa: Z460, Z446
                total_counts.update(cntr)
                nodes_explored += node_count
                files_explored += 1
            self.line('<info>Total {0} nodes in {1} files were explored.</info>'.format(
                nodes_explored,
                files_explored,
            ))
            self.line('Top {0} names are: '.format(num_top))
            for name, counts in total_counts.most_common(num_top):
                self.line('{0} : {1}'.format(name, counts))


def main():
    """Run CLI."""
    command = CountPartsOfSpeechCommand()
    app = cleo.Application()
    app.add(command.default())
    app.run()


if __name__ == '__main__':
    main()
