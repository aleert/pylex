# -*- coding: utf-8 -*-

"""Output log formatters."""
import json
from logging import Filter, Formatter, LogRecord
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


class FileHandlerFilter(Filter):
    """Filter out records that should not be included in JSON or CSV report."""

    def filter(self, record):  # noqa: A003
        """Filter based on counts."""
        if hasattr(record, 'counts'):
            return 1
        return 0


class CSVFormatter(Formatter):
    """Formatter for logging handlers that convert result to CSV and write them to `output_file`."""

    def __init__(self, separator=',', eol='\n'):
        """Output_file should be either a file path or io with write() method."""
        self.SEP = separator
        self.EOL = eol
        super().__init__()

    def format(self, record: LogRecord) -> Text:  # noqa: A003, C901
        """Transform LogRecord to CSV."""
        report = ''
        if not hasattr(record, 'counts'):
            return ''
        if hasattr(record, 'file_name'):
            report += 'Explored file ' + record.file_name + self.EOL
        else:
            report += 'Explored {0} files in {1}{2}'.format(
                record.files_explored, ', '.join(record.modules_explored), self.EOL,
            )
        report += 'Top {0} words are{1}'.format(record.num_top, self.EOL)
        for name, count in record.counts:
            report += name + self.SEP + str(count) + self.EOL
        return report
