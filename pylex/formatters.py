# -*- coding: utf-8 -*-

"""Output log formatters."""
import csv
import json
from logging import Filter, Formatter, LogRecord
from pathlib import Path
from typing import Counter, Text


class JsonFormatter(Formatter):
    """Formatter for logging handlers that converts result to JSON."""

    def format(self, record: LogRecord) -> Text:  # noqa: A003
        """Convert LogRecord with extra data to json for split and single output modes."""
        if not hasattr(record, 'counts'):
            return ''
        counts: Counter = record.counts
        formatted_report = {
            'files_explored': record.files_explored,
            'nodes_explored': record.nodes_explored,
            'modules_explored': record.modules_explored,
            'pt_of_speech': record.pt_of_speech,
            'node_type': record.node_type,
            'num_top': record.num_top,
            'top_names': {name: count for name, count in counts},
        }
        # for splitted output
        if hasattr(record, 'file_name'):
            formatted_report['filename'] = record.file_name
        report = json.dumps(formatted_report, indent=4)
        return report


class JsonHandlerFilter(Filter):
    """Filter that filters records with `counts` property set (used for JSON logging)."""

    def filter(self, record):  # noqa: A003
        """Filter based on counts."""
        if hasattr(record, 'counts'):
            return 1
        return 0


class CSVFormatter(Formatter):
    """Formatter for logging handlers that convert result to CSV and write them to `output_file`."""

    def __init__(self, output_file):
        """Output_file should be either a file path or io with write() method."""
        self.output_file_name = output_file
        super().__init__()

    def format(self, record: LogRecord) -> Text:  # noqa: A003, C901
        """Convert LogRecord with extra data to json for split and single output modes."""
        if isinstance(self.output_file_name, str):
            path = Path(self.output_file_name)
            if not path.exists():
                path.touch()
            writer = csv.writer(path.open(mode='w+'))

        else:
            writer = csv.writer(self.output_file_name)

        if not hasattr(record, 'counts'):
            return ''

        writer.writerow([
            'Explored {0} files in {1}.'.format(
                record.files_explored, ', '.join(record.modules_explored),
            ),
        ])
        writer.writerow(['Top {0} words are'.format(record.num_top)])
        writer.writerow(['name', 'counts'])
        for name, count in record.counts:
            writer.writerow([name, count])

        try:
            writer.close()
        except AttributeError:
            return ''

        return ''
