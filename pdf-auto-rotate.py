#!/usr/bin/python
from subprocess import check_output
from os import remove, rename, path
import sys
import logging

LOG_FILE = 'pdf-auto-rotate.log'
LOG_LEVEL = logging.INFO

logging.basicConfig(filename=LOG_FILE,level=LOG_LEVEL)

# Get the total number of args passed to the demo.py
total = len(sys.argv)

if total != 3:
    logging.error("The only arguments should be input file name and output file name. Wrong number of arguments.")
    sys.exit(-1)

# Get the arguments list 
cmdargs = sys.argv
outfile = cmdargs.pop()
infile = cmdargs.pop()
logging.debug('infile: %s | outfile: %s' % (infile, outfile))

if not path.isfile(infile):
    logging.error("%s file is not a file." % infile)
    sys.exit(-2)

# command to get page dimensions in format:
# "page1w,page1h;page2w,page2h;..;pageNw,pageNh;"
command = ['identify', '-format', '%[fx:w],%[fx:h];', infile]
logging.debug(' '.join(command))

# run command
pages = check_output(command)
logging.debug(pages)

# a list which will contain rotation parameter for each page, empty index 0
# parameter because pdftk page index starts from 1
to_rotate=['',]

# for each page in documment
for page in pages.rstrip(';\n').split(';'):
    # separate to w and h
    page = page.split(',')
    # if w > h
    if (int(page[0]) > int(page[1])):
        # rotate page (pdftk parameter E means rotate 90 degrees)
        to_rotate.append('E')
    else:
        # don't rotate page
        to_rotate.append('')

# construct command to rotate pages
command = ['pdftk', 'A=%s' % infile, 'cat']

# for each page
for i in range(1, len(to_rotate)):
    # append rotation of said page
    command.append(str("A%i%s" % (i, to_rotate[i])))

# append output parameters
command.append('output')
command.append(outfile)
logging.debug(' '.join(command))

# run comand
ret = check_output(command)
logging.debug(ret)
