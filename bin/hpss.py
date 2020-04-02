#!/usr/bin/env python

import os
import sys
import re
import shlex
import subprocess as sp
from collections import OrderedDict
from argparse import ArgumentParser,ArgumentDefaultsHelpFormatter

class HPSS(object):
#{{{
    '''
    Simple HPSS object that performs HPSS related operations such as
    get, copy and move.
    '''

    def __init__(self,verbose=False,**kwargs):
    #{{{
        '''
        Initialize HPSS object
        '''

        self.hsi     = 'hsi'
        self.htar    = 'htar'
        self.verbose = verbose

        return
    #}}}

    def check(self,exit_codes):
    #{{{
        '''
        Check the exit status
        '''

        for exit_code in exit_codes:
            if ( exit_code ):
                print 'unexpected error, exit code = %d' % (exit_code)
                sys.exit(exit_code)

        return
    #}}}

    def command(self,input_files,copy=False,get=False,move=False):
    #{{{
        '''
        Call the relevant HPSS command
        '''

        if   ( get  ): self.get( input_files)
        elif ( copy ): self.copy(input_files)
        elif ( move ): self.move(input_files)

        return
    #}}}

    def stage(self,input_files):
    #{{{
        '''
        Stage files within volume for HPSS operation.
        '''

        if ( self.verbose ): print 'staging ...'

        process = []
        for files in input_files:

            tmp_files = []
            for filename in files: tmp_files.append(filename[0])
            if ( self.verbose ):
                for filename in tmp_files: print ' %s' % filename
            str_len = len(' '.join(tmp_files))
            if ( str_len > 3072 ):
                nfiles  = 3072 / (str_len/len(tmp_files)) - 1
                nstages = len(tmp_files) / nfiles
                subset_tmp_files = [tmp_files[x:x+nfiles] for x in range(0,len(tmp_files),nfiles)]
                for subset in subset_tmp_files:
                    cmd ='%s stage -w %s' % (self.hsi,' '.join(subset))
                    process.append(sp.Popen(shlex.split(cmd),stderr=sp.PIPE,stdout=sp.PIPE))
            else:
                cmd ='%s stage -w %s' % (self.hsi,' '.join(tmp_files))
                process.append(sp.Popen(shlex.split(cmd),stderr=sp.PIPE,stdout=sp.PIPE))

        exit_codes = [p.wait() for p in process]

        self.check(exit_codes)

        return
    #}}}

    def get(self,input_files):
    #{{{
        '''
        Get files from HPSS to local disk
        '''

        self.stage(input_files)

        if ( self.verbose ): print 'getting ...'

        process = []
        for files in input_files:
            for filename in files:

                cmd ='%s -xf %s %s' % (self.htar,filename[0],' '.join(filename[1:]))
                process.append(sp.Popen(shlex.split(cmd),stderr=sp.PIPE,stdout=sp.PIPE))

        exit_codes = [p.wait() for p in process]

        self.check(exit_codes)

        return
    #}}}

    def copy(self,input_files):
    #{{{
        '''
        Copy files from one location in HPSS to another
        This will overwrite files on the destination if they exist
        '''

        self.stage(input_files)

        if ( self.verbose ): print 'copying ...'

        process = []
        for files in input_files:
            for filename in files:

                cmd = '%s mkdir -p %s' % (self.hsi,os.path.dirname(filename[1]))
                hsi = sp.Popen(shlex.split(cmd),stderr=sp.PIPE,stdout=sp.PIPE)
                exit_code = hsi.wait()
                self.check([exit_code])

                cmd ='%s copy -pf %s %s' % (self.hsi,filename[0],filename[1])
                process.append(sp.Popen(shlex.split(cmd),stderr=sp.PIPE,stdout=sp.PIPE))

        exit_codes = [p.wait() for p in process]

        self.check(exit_codes)

        return
    #}}}

    def move(self,input_files):
    #{{{
        '''
        Move files from one location in HPSS to another
        '''

        self.copy(files)

        process = []
        for files in input_files:
            for filename in files:

                cmd ='%s rm -f %s' % (self.hsi,filename[0])
                process.append(sp.Popen(shlex.split(cmd),stderr=sp.PIPE,stdout=sp.PIPE))

        exit_codes = [p.wait() for p in process]

        self.check(exit_codes)

        return
    #}}}
#}}}

def make_dict(input_args):
#{{{
    '''
    Create a dictionary based on input arguments.
    Options include reading a raw txt file, and sort.
    The sorted file can be written out for easy diagnosing time-outs.
    Or read from a sorted txt file, containing files on the same volume.
    '''

    # open and read input filename
    try:
        fh = open(input_args.filename,'r')
        files = fh.readlines()
        fh.close()
    except IOError, err:
        raise IOError(err)

    if ( input_args.read_dict ):
        dict_vol = read_dict(files)
    else:
        if ( input_args.verbose ): print 'sorting ...'
        dict_vol = sort_dict(files)
        for volume in dict_vol.iterkeys():
            if ( input_args.write_dict ):
                write_dict('%s.%s.dict'%(input_args.filename,volume),dict_vol[volume])

    print
    print 'Your files are spread across the following volumes:'
    print 'Volume     # of files'
    for volume in dict_vol.iterkeys():
        print '%s %d' % (volume.ljust(10), len(dict_vol[volume]))
    print

    if ( input_args.write_dict ): sys.exit(0)

    # skip volumes
    for volume in dict_vol.iterkeys():
        if volume in input_args.skip_volumes: dict_vol.pop(volume,None)

    return dict_vol
#}}}

def read_dict(input_files):
#{{{
    '''
    Read filenames on one single volume.
    '''

    filename = input_files[0].strip().split()
    cmd = 'hsi ls -X %s' % (filename[0])
    hsi = sp.Popen(shlex.split(cmd),stderr=sp.PIPE)
    cmd = 'grep "PV List"'
    grep = sp.Popen(shlex.split(cmd),stdin=hsi.stderr,stdout=sp.PIPE)
    o,e = grep.communicate()
    volume = re.findall(r'PV List: (\S+)',o)[0]

    dict_vol = {}
    dict_vol[volume] = []
    for filename in input_files:
        filename = filename.strip().split()
        dict_vol[volume].append([filename[0],' '.join(filename[1:])])

    return dict_vol
#}}}

def write_dict(filename,input_files):
#{{{
    '''
    Write a text file containing filenames in one single volume.
    '''

    try:
        fh = open(filename,'w')
        for file in input_files:
            fh.write(' '.join(file)+'\n')
        fh.close()
    except IOError,err:
        raise IOError(err)

    return
#}}}

def sort_dict(input_files):
#{{{
    '''
    Sort files based on their tape information, specifically PV List
    '''

    # Loop through files, get their volume info and build a dictionary of volumes
    dict_vol = {}
    for filename in input_files:

        filename = filename.strip().split()
        cmd = 'hsi ls -X %s' % (filename[0])
        hsi = sp.Popen(shlex.split(cmd),stderr=sp.PIPE)
        cmd = 'grep "PV List"'
        grep = sp.Popen(shlex.split(cmd),stdin=hsi.stderr,stdout=sp.PIPE)
        o,e = grep.communicate()
        volume = re.findall(r'PV List: (\S+)',o)[0]
        if ( not dict_vol.has_key(volume) ): dict_vol[volume] = []
        dict_vol[volume].append([filename[0],' '.join(filename[1:])])

    # Order the dictionary of volumes by number of files in each volume
    o_dict_vol = OrderedDict(sorted(dict_vol.items(),key=lambda(k,v):len(v),reverse=True))

    return o_dict_vol
#}}}

def main():
#{{{
    '''
    Get / Copy / Move files on HPSS.

    Usage:
    $> hpss.py -h

    To Get:
    $> hpss.py -f file_list -g

    file_list is a file that contains a list of files that need to be fetched from HPSS
    If subfiles are omitted, full tarballs will with fetched.
    eg.
    $> cat file_list
    /path/file1.tar subfile1a subfile1b
    /path/file2.tar subfile2a subfile2b
    /path/file3.tar subfile3a subfile3b
    /path/file4.tar subfile4a subfile4b
    /path/file5.tar subfile5a subfile5b

    To Copy or Move:
    $> hpss.py -f file_list -c
    $> hpss.py -f file_list -m

    file_list is a file that contains a list of files that need to be copied / moved from old to new location
    move implies copy and then remove
    eg.
    $> cat file_list
    /old/path/file1.tar /new/path/file1.tar
    /old/path/file2.tar /new/path/file2.tar
    /old/path/file3.tar /new/path/file3.tar
    /old/path/file4.tar /new/path/file4.tar
    /old/path/file5.tar /new/path/file5.tar
    '''

    parser = ArgumentParser(description='smartly get/copy/move files from or within HPSS',formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f','--filename',help='filename containing list of files to get/copy/move on HPSS',required=True)
    parser.add_argument('-v','--verbose',help='verbose',action='store_true',required=False)
    parser.add_argument('-s','--skip_volumes',type=str,nargs='+',default=[],required=False)
    parser.add_argument('-n','--nsimul',help='number of simultaneous HPSS operations',type=int,default=1,required=False)
    parser.add_argument('-w','--write_dict',help='write sorted dictionary',action='store_true',required=False)
    parser.add_argument('-r','--read_dict',help='read sorted dictionary, if so, skip sorting',action='store_true',required=False)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-g','--get', help='get', action='store_true',required=False)
    group.add_argument('-c','--copy',help='copy',action='store_true',required=False)
    group.add_argument('-m','--move',help='move',action='store_true',required=False)
    args = parser.parse_args()

    # Initialize the HPSS object
    hpss = HPSS(verbose=args.verbose)

    # Get the dictionary of volumes, with files within each volume
    dict_vol = make_dict(args)

    nsimul = args.nsimul
    if ( nsimul > len(dict_vol) ): nsimul = len(dict_vol)

    ntran = 0
    files = []
    for volume in dict_vol.iterkeys():

        print 'Volume: %s ( %d )' % (volume,len(dict_vol[volume]))

        ntran += 1

        files.append(dict_vol[volume])
        if ( ntran < nsimul ): continue

        # First stage and then perform desired operation
        hpss.command(files,copy=args.copy,get=args.get,move=args.move)

        ntran = 0
        files = []

        print

#}}}

if __name__ == '__main__': main()
