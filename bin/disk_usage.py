#!/usr/bin/env python

###############################################################
# disk_usage.py - spit out disk usage based on user group on Theia
###############################################################

import os
import sys
import subprocess
import grp
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

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

quotadb = "/scratch3/BMC/public/quotas"

for group in groups:
    if group in ['rstprod']:
        continue
    fname = '%s/%s' % (quotadb, group)
    if not os.path.isfile(fname):
        continue
    print("\033[1;36m================================================================\033[0m")
    print("          \033[1;34m Project: \033[5;41;1;37m %s \033[0m" % group)
    cmd = 'cat %s | head -n %d' % (fname, nlines)
    try:
        subprocess.check_call(cmd, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        print(e.output)
    print("\033[1;36m================================================================\033[0m")

sys.exit(0)
