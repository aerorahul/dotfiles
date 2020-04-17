#!/usr/bin/env python3

import os
import sys
import subprocess
import time
import datetime
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


def detect_defaults():

    defs = {}

    if os.path.isdir("/nwprod"):  # wcoss
        defs['machine'] = 'wcoss'
        defs['queues'] = ['debug', 'debug2', 'dev',
                          'dev2', 'transfer', 'predev', 'predev2']
        defs['accounts'] = ['FV3GFS-T2O', 'GFS-T2O']
        defs['npe_node_max'] = 24
        defs['scheduler'] = 'lsf'

    if os.path.isdir("/work"):  # orion
        defs['machine'] = 'orion'
        defs['queues'] = ['debug', 'urgent', 'batch', 'windfall', 'novel']
        defs['accounts'] = ['da-cpu', 'fv3-cpu']
        defs['partitions'] = ['orion', 'debug', 'bigmem', 'service']
        defs['npe_node_max'] = 40
        defs['scheduler'] = 'slurm'

    elif os.path.isdir("/scratch1"):  # hera
        defs['machine'] = 'hera'
        defs['queues'] = ['debug', 'batch', 'urgent', 'windfall',
                          'fgedebug', 'fgebatch']
        defs['accounts'] = ['da-cpu', 'fv3-cpu']
        defs['partitions'] = ['hera', 'bigmem', 'service', 'fge']
        defs['npe_node_max'] = 40
        defs['scheduler'] = 'slurm'

    elif os.path.isdir("/discover"):  # discover
        defs['machine'] = 'discover'
        defs['queues'] = ['debug', 'inter']
        defs['accounts'] = ['g0613', 's0818', 'gmaoint', 'm2val', 'j1068']
        defs['partitions'] = ['compute', 'datamove']
        defs['npe_node_max'] = 24
        defs['scheduler'] = 'slurm'

    else:
        raise SystemExit("Unsupported machine, ABORT!")

    return defs


def check_input_arguments(PBS):

    def _abort(msg):
        raise SystemExit(msg)

    x = time.strptime(PBS.walltime, '%H:%M:%S')
    wseconds = datetime.timedelta(
        hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec).seconds

    if PBS.machine in ['hera']:
        if PBS.queue in ['debug'] and wseconds > 30*60:
            msg = f"Queue {PBS.queue} on {PBS.machine} does not allow more than 30 minutes of walltime, ABORT!"
            raise SystemExit(msg)
        elif PBS.queue in ['bigmem'] and PBS.nodes > 6:
            msg = f'Queue {PBS.queue} on {PBS.machine} does not support more than 6 nodes, ABORT!'
            raise SystemExit(msg)

    elif PBS.machine in ['orion']:
        if PBS.queue in ['debug'] and wseconds > 30*60:
            msg = f"Queue {PBS.queue} on {PBS.machine} does not allow more than 30 minutes of walltime, ABORT!"
            raise SystemExit(msg)

    elif PBS.machine in ['discover']:
        if PBS.queue in ['debug'] and wseconds > 60*60:
            msg = f"Queue {PBS.queue} on {PBS.machine} does not allow more than 60 minutes of walltime, ABORT!"
            raise SystemExit(msg)

    return


def submit_interactive_job(PBS):

    inodes = int(PBS.nproc/PBS.ppn)
    PBS.nodes = inodes+1 if inodes*PBS.ppn < PBS.nproc else inodes
    PBS.nproc = PBS.nodes * PBS.ppn

    if PBS.scheduler in ['slurm']:
        PBS.X = '--x11' if PBS.enable_x else ''
        PBS.mail = '--mail-type BEGIN --mail-user %s' % PBS.mailto if PBS.alert else ''

    elif PBS.scheduler in ['lsf']:
        PBS.X = '-XF' if PBS.enable_x else ''
        PBS.mail = '-B -u %s' % PBS.mailto if PBS.alert else ''

    if PBS.machine in ['hera']:
        PBS.partition = 'hera'

    elif PBS.machine in ['orion']:
        PBS.partition = 'debug' if PBS.queue in ['debug'] else 'orion'

    elif PBS.machine in ['discover']:
        PBS.partition = 'compute'
        PBS.X = ''

    elif PBS.machine in ['wcoss']:
        PBS.X = ''

    check_input_arguments(PBS)

    print(f'Requesting an interactive job on {PBS.machine} ({PBS.scheduler}) with the following resources:')
    print(f'    queue : {PBS.queue}')
    print(f' walltime : {PBS.walltime}')
    print(f'   nprocs : {PBS.nproc}')
    print(f'    nodes : {PBS.nodes}')
    print(f'      ppn : {PBS.ppn}')
    print(f'  account : {PBS.account}')
    mailTo = f'To: {PBS.mailto}' if PBS.alert else ''
    print(f'    alert : {PBS.alert} {mailTo}')
    print(f'X forward : {"yes" if PBS.enable_x else "no"}')
    print(f'directory : {PBS.directory}')

    if PBS.scheduler in ['slurm']:
        cmd = f"salloc --partition={PBS.partition} --qos={PBS.queue} --account={PBS.account} --nodes={PBS.nodes} --ntasks-per-node={PBS.ppn} --time={PBS.walltime} --chdir={PBS.directory} --job-name=InteractiveJob"

    elif PBS.scheduler in ['lsf']:
        cmd = f"bsub -Is {PBS.X} -J InteractiveJob -P {PBS.account} -q {PBS.queue} -W {PBS.walltime[:5]} -a poe -n {PBS.nproc} -R 'span[ptile={PBS.ppn}]' -R 'affinity[core(2)]' {PBS.mail} bash"

    if PBS.verbose:
        print(cmd)
    os.system(cmd)

    return


if __name__ == "__main__":
    '''run_iJob.py - Request an interactive job on Hera / WCOSS / Discover'''

    defs = detect_defaults()

    parser = ArgumentParser(description=f'Run an interactive job on {defs["machine"]}',
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-q', '--queue', help='requested queue name', type=str,
                        choices=defs['queues'], default=defs['queues'][0], required=False)
    parser.add_argument('-A', '--account', help='account to charge', type=str,
                        choices=defs['accounts'], default=defs['accounts'][0], required=False)
    parser.add_argument('-w', '--walltime', help='requested walltime',
                        type=str, default='00:30:00', metavar='HH:MM:SS', required=False)
    parser.add_argument('-n', '--nproc', help='requested number of processors',
                        type=int, default=12, required=False)
    parser.add_argument('-p', '--ppn', help='requested number of processors per node',
                        type=int, choices=range(1, defs['npe_node_max']+1), default=12, required=False)
    parser.add_argument('-a', '--alert', help='send an alert when job starts',
                        action='store_true', required=False)
    parser.add_argument('-M', '--mailto', help='if alert enabled, send an email alert to', type=str,
                        default=os.environ['REPLYTO'], choices=['2068494572@txt.att.net', os.environ['REPLYTO']], required=False)
    parser.add_argument('-X', '--enable_x', help='enable X forwarding',
                        action='store_false', required=False)
    parser.add_argument('-d', '--directory', help='change to desired working directory',
                        type=str, default=os.environ['PWD'], required=False)
    parser.add_argument('-v', '--verbose', help='print debugging information',
                        action='store_true', required=False)
    PBS = parser.parse_args()

    PBS.machine = defs['machine']
    PBS.scheduler = defs['scheduler']

    submit_interactive_job(PBS)

    sys.exit(0)

