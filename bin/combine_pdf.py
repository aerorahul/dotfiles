#!/usr/bin/env python

###############################################################
# combine_pdf.py - script used to combine multiple pdf's into one
###############################################################

import os, sys, subprocess
from argparse import ArgumentParser,ArgumentDefaultsHelpFormatter

parser = ArgumentParser(description = 'Combine multiple pdf files into one',formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('-i','--input',help='input files',nargs='+',required=True)
parser.add_argument('-o','--output',help='output file',type=str,default='test.pdf',required=False)
args = parser.parse_args()

input_files = ' '.join(args.input)
output_file = args.output

if os.path.exists(output_file):
    print '%s exists ...' % output_file
    input = raw_input('overwrite %s? yes or no: ' % output_file)
    if ( input.lower() not in ['y','yes'] ): sys.exit(0)

cmd = 'gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=%s %s' % (output_file, input_files)

try:
    subprocess.check_call(cmd,stderr=subprocess.STDOUT,shell=True)
except subprocess.CalledProcessError as e:
    print e.output

sys.exit(0)
