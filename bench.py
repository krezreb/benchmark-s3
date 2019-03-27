#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, json
import argparse
import shutil
import random

import datetime

parser = argparse.ArgumentParser()
parser.add_argument('--width', default=10, help='How many root folders to create')
parser.add_argument('--depth', default=10, help='What depth of subfolders to create')
parser.add_argument('--files', default=10, help='How many files to create scattered across nodes')
parser.add_argument('--file-size-bytes', default=10, help='Size of files to create')
parser.add_argument('--root', default=None, help='What working directory to benchmark')
parser.add_argument('--quiet', action='store_true', default=False, help='No output')
parser.add_argument('--keep', action='store_true', default=False, help='Keep files after run?')

args = parser.parse_args()

def log(s):
    if args.quiet:
        return
    print("BENCHMARK: {}".format(s))

root = args.root

if root == None:
    root = './'

dirs = []
endpoint_dirs = []


for w in range(0, int(args.width)):
    line = ["w{}".format(w)]
    for d in range(0, int(args.depth)):
        line.append("d{}".format(d))
        dirs.append("/".join(line))

    endpoint_dirs.append("/".join(line))


log("Making {} dirs in {}".format(len(dirs), root))
for d in endpoint_dirs:
    path = root+'/.bench/'+d
    if not os.path.isdir(path):
        log(path)
        os.makedirs(path)

chosen_endpoints = []

log("Making {} files each weighing {}kb in dirs".format(args.files, args.file_size_bytes))
for fnum in range(0, int(args.files)):
    which = random.choice(endpoint_dirs)
    path = root+'/.bench/'+which
    with open(path+'/file{}.dat'.format(fnum), 'wb') as fh:
        fh.write(os.urandom(int(args.file_size_bytes)))
        
    chosen_endpoints.append(which)

for d in chosen_endpoints:
    path = root+'/.bench/'+d
    files = []
    for f in os.listdir(path):
        files.append(f)
    log(d)
    log(files)
    
if not args.keep:
    log("Deleting {} dirs in {}".format(len(dirs), root))
    shutil.rmtree(root+'/.bench/')
        

