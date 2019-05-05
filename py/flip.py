# 2019/01/08 arichardson: flip (reorder) columns in csv with header
# nested commas tolerated!
import os
import sys
import csv
from misc import *
import time; t = time.time(); print t
csv.register_dialect('my',
                     delimiter=",",
                     quoting=csv.QUOTE_ALL,
                     skipinitialspace=True)

infile = sys.argv[1]
f = open(infile)
before = f.readline().strip().split(",")
for i in range(0, len(before)):
    before[i] = before[i].strip()
f.close()

# infile = "Merged_SDPR_for_clustering.csv"
#before = ['"FILEID"','"YM"','"STUDYID"','"PROGRAM"','"AGE"','"FAMTYPE"','"DPNO"','"PAY"','"POSTCD_3D"']
#after = ['"FILEID"','"YM"','"PROGRAM"','"AGE"','"FAMTYPE"','"DPNO"','"PAY"','"POSTCD_3D"','"STUDYID"']

after = sys.argv[2:]
for i in range(0, len(after)):
    after[i] = after[i].strip('"')
    after[i] = after[i].strip()

print "before", before
print "after", after

bi, ai = {}, {}
for i in range(0, len(before)):
    bi[before[i]] = i
for i in range(0, len(before)):
    ai[i] = bi[after[i]]

keep_i = []
outfile = infile+"_flip.csv"; of = open(outfile, "wb")
f, ci, f_names, n_f, fields = open(infile), 0, None, 0, None
tt = time.time()
ttt = None
while True:
    line = f.readline()
    if not line:
        break
    line = line.strip()
    if ci == 0:
        f_names = line.split(","); print f_names
        n_f, fields = len(f_names), ",".join(f_names)
        if n_f != len(before) or n_f != len(after):
            err("")
    w = line.split(",")
    if len(w) != n_f:
        g=open("tmp.csv","wb"); g.write(fields+"\n"+line); g.close()
        reader = csv.reader(open("tmp.csv"), dialect='my')
        hdr, lin = reader
        w = lin
    if len(w) != n_f:
        err("")
    # write out flipped line..
    for i in range(0, n_f):
        if i>0:
            of.write(",")
        of.write(w[ai[i]].strip('"'))
    of.write("\n")
    ci += 1
    if ci % 1000 == 0:
        ttt = tt
        tt = time.time()
        print ci/1000, "k, S/k: ", tt-ttt
print "done"
print "  ", int((ci / (time.time() - t))/1000.), "K lines per sec"
f.close(); of.close()
