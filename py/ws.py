#!/usr/bin/env python2.7
''' ws.py: remove trailing whitespace and systematic left-whitespace'''

import os
import sys
import ntpath
from misc import *

args, max_spaces = sys.argv, 0
if len(args) < 2:
    msg = 'ws.py: usage: ws.py [input file name].\n\t'
    err(msg + 'removes trailing right-space and systematic left-space')

def f_base(fn):
    return ntpath.basename(fn)

try:
    fn = os.path.abspath(args[1].strip())
except:
    err('could not parse filename')

if not exists(fn):
    err('file [' + str(fn) + '] not found.')

lines = open(fn).readlines()
for i in range(0, len(lines)):
    lines[i] = lines[i].rstrip()
    l_i = lines[i]
    l_spaces = len(l_i) - len(l_i.lstrip())
    if(l_spaces > max_spaces):
        max_spaces = l_spaces

min_spaces = max_spaces
for i in range(0, len(lines)):
    l_i = lines[i]
    l_spaces = len(l_i) - len(l_i.lstrip())
    if(l_spaces < min_spaces):
        if(l_i.strip() != ''):
            min_spaces = l_spaces

print "min_spaces", min_spaces
head, tail = ntpath.split(fn)
head = head.strip() + '/'
head = os.path.abspath(head) + '/'
print 'head', head
bfn = fn + '.bak'  # head + '.' + f_base(fn)
print 'bfn', bfn

# save a backup
open(bfn, 'wb').write(open(fn).read())
printw(bfn)

write_ln = []
for i in range(0, len(lines)):
    line = lines[i]
    write_ln.append(line[min_spaces:])

# write the result.
open(fn, 'wb').write(('\n').join(write_ln))
printw(fn)