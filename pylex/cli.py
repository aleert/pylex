# -*- coding: utf-8 -*-

"""CLI interface."""
import argparse
import collections
import logging
from typing import Counter, Dict, NewType, Tuple, cast

from pylex.file_handlers import get_all_py
from pylex.formatters import CSVFormatter, FileHandlerFilter, JsonFormatter
from pylex.visit_nodes import count_pt_of_speech_in_tree


def prepare_parser() -> argparse.ArgumentParser:  # noqa: Z213
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
    Node type to explore. 
    """
    parser.add_argument(
        '-N',
        '--node-type',
        default='FunctionDef',
        choices=('FunctionDef', 'function', 'ClassDef', 'class', 'Assign', 'assign'),
        help=node_type_help,
    )

    parser.add_argument(
        '-O',
        '--output',
        help='Output file name or path.',
    )

    parser.add_argument(
        '-S',
        '--split',
        action='store_true',
        help='Generate output for every file explored',
    )

    parser.add_argument(
        '-v',
        action='store_true',
        help='Log entry while processing every file.',
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--json',
        action='store_true',
        help='JSON output.',
    )

    group.add_argument(
        '--csv',
        action='store_true',
        help='CSV output.',
    )

    return parser


# for type hinting
FileName = NewType('FileName', str)
NodeNameCounter = NewType('NodeNameCounter', Counter[str])
TotalNodeNamesCount = NewType('TotalNodeNamesCount', int)
AllFilesEntry = Tuple[NodeNameCounter, TotalNodeNamesCount]
AllFiles = Dict[FileName, AllFilesEntry]


def process_with_split_output(  # noqa: Z210
    all_files: AllFiles,
    num_top: int,
    **kwargs,
) -> None:
    """Make counts from all_files for separate output for each file."""
    for filename, (cntr, node_count) in all_files.items():  # noqa: Z460, Z446
        # for json formatter
        extra_info = {
            'num_top': num_top,
            'counts': cntr.most_common(num_top),
            'files_explored': 1,
            'nodes_explored': node_count,
            'file_name': filename,
        }
        extra_info.update(kwargs)
        logging.info(
            '{0} nodes explored in file {1}'.format(
                node_count,
                filename,
            ),
            extra=extra_info,
        )
        logging.info('Top {0} names are:'.format(num_top))
        for name, counts in cntr.most_common(num_top):
            logging.info('{0} : {1}'.format(name, counts))


def process_with_single_output(  # noqa: Z210
    all_files: AllFiles,
    num_top: int,
    **kwargs,
) -> None:
    """Make counts from all_files for joined output."""
    total_counts = collections.Counter()
    nodes_explored = 0
    files_explored = 0
    for _filename, (cntr, node_count) in all_files.items():  # noqa: Z460, Z446
        total_counts.update(cntr)
        nodes_explored += node_count
        files_explored += 1

    # for json formatter
    extra_info = {
        'num_top': num_top,
        'counts': total_counts.most_common(num_top),
        'files_explored': files_explored,
        'nodes_explored': nodes_explored,
    }
    extra_info.update(kwargs)
    logging.info(
        'Total {0} nodes in {1} files were explored.'.format(
            nodes_explored,
            files_explored,
        ),
        extra=extra_info,
    )

    logging.info('Top {0} names are: '.format(num_top))
    for name, counts in total_counts.most_common(num_top):
        logging.info('{0} : {1}'.format(name, counts))


def make_logger(
    logging_level: int,
    is_json: bool = False,
    is_csv: bool = False,
    filename: str = None,
) -> logging.Logger:
    """Set appropriate handler and logger."""
    logger = logging.getLogger()
    logger.setLevel(logging_level)

    ch = logging.StreamHandler()

    if filename:
        ch = logging.FileHandler(filename=filename)

    if is_json:
        ch.setFormatter(JsonFormatter('%(message)s'))
        ch.addFilter(FileHandlerFilter())

    if is_csv:
        ch.setFormatter(CSVFormatter())
        ch.addFilter(FileHandlerFilter())

    ch.setLevel(logging_level)
    logger.addHandler(ch)

    return logger


def main():  # noqa: Z210
    """Parse args and print output."""
    parser = prepare_parser()
    args = parser.parse_args()
    logging_level = logging.INFO
    if args.v:
        logging_level = logging.DEBUG

    make_logger(logging_level, filename=args.output, is_json=args.json, is_csv=args.csv)

    all_files = {}  # type: AllFiles

    try:
        for py_file in get_all_py(args.modules, write_log=True):

            all_files[cast(FileName, str(py_file))] = cast(
                AllFilesEntry,
                count_pt_of_speech_in_tree(
                    py_file,
                    target_part=args.pt_of_speech,
                    node_types=[args.node_type],
                    exclude_dunder=True,
                    exclude_private=False,
                ),
            )
    except (OSError, FileNotFoundError) as error:
        logging.error('<error>' + str(error) + '</error>')

    if args.split:
        process_with_split_output(
            all_files,
            num_top=args.top,
            pt_of_speech=args.pt_of_speech,
            node_type=args.node_type,
            modules_explored=args.modules,
        )

    else:
        process_with_single_output(
            all_files,
            num_top=args.top,
            pt_of_speech=args.pt_of_speech,
            node_type=args.node_type,
            modules_explored=args.modules,
        )


if __name__ == '__main__':
    main()
