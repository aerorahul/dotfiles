#!/usr/bin/env python3

import os
import sys
import re
import logging
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

LEVEL = 'INFO'
FORMAT = '%(asctime)s - %(levelname)-8s - %(name)-8s: %(message)s'
logging.basicConfig(level=LEVEL, format=FORMAT)
logger = logging.getLogger('compare_diff')

_DIFFER_RE=re.compile(
    r"(?P<files>Files)\s(?P<left>\S*)\s(and)\s(?P<right>\S*)\s(differ)"
    )
_ONLY_RE=re.compile(
    r"(?P<only>Only in)\s(?P<directory>\S*)\s(?P<filename>\S*)"
    )

parser = ArgumentParser(description='Perform diff on files recursively through a directory',
                        formatter_class=ArgumentDefaultsHelpFormatter)

parser.add_argument('-f', '--filename', type=str, default='file.diff',
                    required=True,
                    help='name of the file containing the output of diff -r')
parser.add_argument('-d', '--diff', type=str, default='diff',
                    required=False,
                    choices=['diff', 'colordiff', 'xxdiff', 'vimdiff'],
                    help='name of the diff command to use')
parser.add_argument('-v', '--verbose', action='store_true',
                    required=False,
                    help='print with verbosity')

args = parser.parse_args()

if args.verbose:
    logger.setLevel(level='DEBUG')

with open(args.filename, 'r') as fh:
    for line in fh:
        line = line.strip()
        differ = _DIFFER_RE.match(line)
        if differ:
            left_file, right_file = differ.groupdict()['left'], differ.groupdict()['right']
            cmd = f"{args.diff} {left_file} {right_file}"

            msg = f'Showing diffs between: {left_file} and {right_file}'
            logger.info("="*80)
            logger.info(msg)
            logger.info("*"*80)
            os.system(cmd)
            logger.info("="*80)
            to_continue = input("Continue to next diff? [Y/n]: ")
            logger.info(' ')
            if to_continue.upper() in ['Y', 'YES', '']:
                logger.info('continuing to next file ...')
                logger.info(' ')
                continue
            else:
                logger.info('bye ...')
                logger.info(' ')
                break

logger.info('done ...')

