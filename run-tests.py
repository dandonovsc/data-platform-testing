#!/usr/bin/env python3

import argparse
import subprocess

import sys


def main():
    parser = argparse.ArgumentParser(description='Wrapper around unittest python command.')

    parser.add_argument('--environment', '-e',
                        type=str,
                        dest="environment",
                        choices=('local', 'dev', 'qa',
                                 'stage', 'prod'),
                        default='local',
                        help='The environment to run the script against.')
    parser.add_argument('--directory', '-d',
                        type=str,
                        dest="directory",
                        default='tests',
                        help='The directory from which tests should be scanned for.')
    parser.add_argument('--file', '-f',
                        type=str,
                        dest="file",
                        help='The individual file to run.')

    args = parser.parse_args()
    if args.file:
        tests_to_run = args.file
    else:
        tests_to_run = f'discover {args.directory}'


    COMMAND = f'NAMESPACE={args.environment} /usr/bin/env python3 -W ignore -m unittest {tests_to_run} -v'
    p = subprocess.call(COMMAND, shell=True)
    sys.exit(p)


if __name__ == '__main__':
    main()
