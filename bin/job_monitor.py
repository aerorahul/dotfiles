#!/usr/bin/env python

import sys
import subprocess
import time
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


def main():

    global verbose, machine
    all_machines = ['zeus', 'theia', 'wcoss',
                    'gyre', 'tide', 'wcoss_c', 'luna', 'surge']

    parser = ArgumentParser(description='monitor status of job(s)',
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-j', '--jobid', help='job identifier(s)',
                        type=str, nargs='+', required=True)
    parser.add_argument('-m', '--machine', help='machine', type=str,
                        choices=all_machines, default=all_machines[1], required=False)
    parser.add_argument('-v', '--verbose', help='verbose',
                        action='store_true', required=False)
    parser.add_argument('-s', '--sleep', help='sleep interval (in seconds)',
                        type=int, default=30, required=False)
    args = parser.parse_args()

    jobids = args.jobid
    machine = args.machine
    verbose = args.verbose
    sleepsecs = args.sleep

    while (len(jobids) > 0):
        jobids = job_status(jobids)
        if (len(jobids) > 0):
            time.sleep(sleepsecs)

    sys.exit(0)


def job_status(jobids):

    jobids_tmp = []

    for jobid in jobids:

        if (machine in ['zeus', 'theia']):
            cmd = "qstat -f %s -1 | grep job_state | cut -d= -f2 | cut -d' ' -f2" % jobid
        elif (machine in ['wcoss', 'wcoss_c', 'gyre', 'tide', 'luna', 'surge']):
            cmd = "bjobs -o 'stat:' -noheader %s" % jobid

        try:
            job_state = subprocess.check_output(cmd, shell=True).strip()
        except subprocess.CalledProcessError as err:
            raise subprocess.CalledProcessError(err)

        if job_state in ['C', 'DONE']:
            if verbose:
                print('%s completed' % jobid)
        else:
            jobids_tmp.append(jobid)

    return jobids_tmp


if __name__ == '__main__':
    main()
