# -*- coding: utf-8 -*-

"""CLI interface."""
import argparse
import collections
from typing import Counter, Dict, NewType, Tuple, cast

from file_handlers import count_pt_of_speech_in_tree, get_all_py, tree_from_py_file_path


def prepare_parser() -> argparse.ArgumentParser:
    """Initialize parser with arguments."""
    description = """Count parts of speech you specify in packages.
                  If no pt_of_speech provided, verb (VB) is used.
                  """

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        'modules',
        nargs='+',
        type=str,
        metavar='PATHS',
        help='Packages or paths you want to explore',
    )

    parser.add_argument(
        '--top',
        type=int,
        default=10,
        help='Print only top most common words.',
    )

    pt_of_speech_help = """
    Part of speech as of nltk.help.upenn_tagset() (NN for noun,
    VB for verb, CD for cardinal etc.)
    """
    parser.add_argument(
        '-P',
        '--pt-of-speech',
        dest='pt_of_speech',
        default='VB',
        help=pt_of_speech_help,
    )

    node_type_help = """
    Node type to explore. FunctionDef, AsyncFunctionDef and ClassDef
    are currently accepted. }
    """
    parser.add_argument(
        '-N',
        '--node-type',
        dest='node_type',
        default='FunctionDef',
        choices=('FunctionDef', 'ClassDef', 'AsyncFunctionDef'),
        help=node_type_help,
    )

    parser.add_argument(
        '-S',
        '--split',
        action='store_true',
        help='Generate output for every file explored',
    )

    return parser


# for type hinting
FileName = NewType('FileName', str)  # noqa: N806
NodeNameCounter = NewType('NodeNameCounter', Counter[str])  # noqa: N806
TotalNodeNamesCount = NewType('TotalNodeNamesCount', int)  # noqa: N806
AllFilesEntry = Tuple[NodeNameCounter, TotalNodeNamesCount]
AllFiles = Dict[FileName, AllFilesEntry]


def process_with_split_output(
    all_files: AllFiles,
    num_top: int,
    logger=None
) -> None:
    """Make counts from all_files for separate output for each file."""
    for filename, (cntr, node_count) in all_files.items():  # noqa: Z460, Z446
        print('<info>{0} nodes explored in file {1}</info>'.format(
            node_count,
            filename,
        ))
        print('Top {0} names are:'.format(num_top))
        for name, counts in cntr.most_common(num_top):
            print('{0} : {1}'.format(name, counts))


def process_with_single_output(
    all_files: AllFiles,
    num_top: int,
    logger=None
) -> None:  # noqa: Z210
    """Make counts from all_files for joined output."""
    total_counts = collections.Counter()
    nodes_explored = 0
    files_explored = 0
    for _filename, (cntr, node_count) in all_files.items():  # noqa: Z460, Z446
        total_counts.update(cntr)
        nodes_explored += node_count
        files_explored += 1
    print('<info>Total {0} nodes in {1} files were explored.</info>'.format(
        nodes_explored,
        files_explored,
    ))
    print('Top {0} names are: '.format(num_top))
    for name, counts in total_counts.most_common(num_top):
        print('{0} : {1}'.format(name, counts))


def main():  # noqa: Z210
    """Parse args and print output."""
    parser = prepare_parser()
    args = parser.parse_args()

    all_files = {}  # type: AllFiles

    try:
        for filepath in get_all_py(args.modules):
            tree, filename = tree_from_py_file_path(filepath)

            all_files[cast(FileName, filename)] = cast(AllFilesEntry, count_pt_of_speech_in_tree(
                tree,
                target_part=args.pt_of_speech,
                node_type=args.node_type,
            ))
    except OSError as error:
        print('<error>' + str(error) + '</error>')

    if args.split:
        process_with_split_output(all_files, num_top=args.top)

    else:
        process_with_single_output(all_files, num_top=args.top)


if __name__ == '__main__':
    main()
