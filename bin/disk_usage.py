#!/usr/bin/env python3

###################################################################
# disk_usage.py - spit out disk usage based on user group on RDHPCS
###################################################################

import os
import sys
import subprocess
import grp
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


_colors = {'blue': '\033[1;34m',
           'cyan': '\033[1;36m',
           'red': '\033[5;41;1;37m',
           'reset': '\33[0m'}

_groups = [g.gr_name for g in grp.getgrall() if os.environ['USER'] in g.gr_mem]

parser = ArgumentParser(description='Spit out the disk usage',
                        formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('-n', '--nusers', help='number of top users',
                    type=int, default=0, required=False)
parser.add_argument('-g', '--groups', help='groups to see disk usage',
                    nargs='+', default=_groups, required=False)
parser.add_argument('-s', '--stmp', help='show stmp usage',
                    action='store_true', required=False)
args = parser.parse_args()

if (args.nusers == 0):
    nlines = 8
elif (args.nusers < 0):
    nlines = 1e10
else:
    nlines = args.nusers + 10
groups = args.groups + ['stmp%d' %
                        i for i in range(1, 5)] if (args.stmp) else args.groups

quotadb = "/scratch2/BMC/public/quotas"

for group in groups:
    if group in ['rstprod']:
        continue
    fname = f'{quotadb}/{group}'
    if not os.path.isfile(fname):
        continue
    print(f"{_colors['cyan']} {'='*80} {_colors['reset']}")
    print(f"\t\t{_colors['blue']}\tProject:\t{_colors['red']}{group}{_colors['reset']}")
    cmd = f'cat {fname} | head -n {nlines}'
    try:
        subprocess.check_call(cmd, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        print(e.output)
    print(f"{_colors['cyan']} {'='*80} {_colors['reset']}")

sys.exit(0)
