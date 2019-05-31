""" >> LogCat parsing tool <<

Returns log lines which match or does not match particular words. It also
can display test duration time between 'TEST STARTED' and 'TEST FINISHED'
phrases found in log file.

To use this tool as a word matcher there are two options:
(1) to return lines that include desired words: -i / --include
(2) to return lines that does not include any of desired words: -e / --exclude

It is possible to have it separately or combined:
python logcat_parser.py <path_to_logcat_file> -i word1,word2,word3
python logcat_parser.py <path_to_logcat_file> -i word1 -e word2,word3

NOTE: Keep in mind, words are separated with commas, without blank chars.

To display the test time duration between 'TEST STARTED' and 'TEST FINISHED'
phrases found in log file, use -s parameter:

python logcat_parser.py <path_to_logcat_file> -s
"""

from sys import exit
from os import path
from argparse import ArgumentParser
from re import compile, error
from datetime import datetime


def _get_args():
    parser = ArgumentParser(description=__doc__)

    parser.add_argument(dest='path', help='Path to the logcat file.')
    parser.add_argument('-i', '--include', dest='include', action='store', metavar='INCLUDED_WORD[,INCLUDED_WORD]',
                        help='Prints out lines that contain provided, comma separated words')
    parser.add_argument('-e', '--exclude', dest='exclude', action='store', metavar='EXCLUDED_WORD[,EXCLUDED_WORD]',
                        help='Prints out lines that does not contain provided, comma separated words')
    parser.add_argument('-s', dest='test_duration', action='store_true', help='Prints out the test time duration')

    args = parser.parse_args()
    args.include = args.include.split(',') if args.include else None
    args.exclude = args.exclude.split(',') if args.exclude else None

    return args


def _get_timestamp_from_line(line):
    re_timestamp = compile('^([0-9-]+ [0-9:.]+)')
    timestamp_pattern = '%m-%d %H:%M:%S.%f'

    try:
        timestamp_string = str(re_timestamp.search(line).group(1)) + '000'
        return datetime.strptime(timestamp_string, timestamp_pattern)
    except (AttributeError, error):
        print(f'Timestamp at line "{line.rstrip()}" is not in correct format: {timestamp_pattern}')
        exit(3)


def _get_test_duration(file_path):
    re_test_start = compile('TEST STARTED')
    re_test_finished = compile('TEST FINISHED')
    start_time = None

    with open(file_path, 'r') as logfile:
        for line in logfile:
            if not start_time and re_test_start.search(line):
                start_time = _get_timestamp_from_line(line)
                continue

            if start_time and re_test_finished.search(line):
                print(f'Test duration: {str(_get_timestamp_from_line(line) - start_time)[:-3]}')
                return 0

    print('No "TEST STARTED" and/or "TEST FINISHED" text sequences in log file.')
    return 4


def _get_log_lines(file_path, included_words, excluded_words):
    log_lines = list()
    re_included_words = [compile(word) for word in included_words] if included_words else []
    re_excluded_words = [compile(word) for word in excluded_words] if excluded_words else []
    all_excluded = True

    with open(file_path, 'r') as logfile:
        for line in logfile:
            for word in re_included_words:
                if word.search(line):
                    log_lines.append(line)
                    break

            for word in re_excluded_words:
                if word.search(line):
                    all_excluded = False
                    break

            if all_excluded:
                log_lines.append(line)
            all_excluded = True

    print(''.join(log_lines))
    return 0


def main():
    args = _get_args()

    if not args.path:
        print(f'Please provide path to logcat file.')
        return 1

    if not path.exists(args.path):
        print(f'Desired path "{args.path}" does not exist.')
        return 2

    if args.test_duration:
        return _get_test_duration(args.path)

    return _get_log_lines(args.path, args.include, args.exclude)


if __name__ == '__main__':
    exit(main())
