#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, json
import argparse
import shutil
import random, time

import datetime
from collections import OrderedDict

parser = argparse.ArgumentParser()
parser.add_argument('--width', default=10, help='How many root folders to create')
parser.add_argument('--depth', default=10, help='What depth of subfolders to create')
parser.add_argument('--runs', default=1, help='How many runs to do')
parser.add_argument('--run-step', default=1, help='Between each run, multiply width by 1*run-step')
parser.add_argument('--files', default=10, help='How many files to create scattered across nodes')
parser.add_argument('--file-size-bytes', default=10, help='Size of files to create')
parser.add_argument('--path', default=None, help='What working directory to benchmark')
parser.add_argument('--quiet', action='store_true', default=False, help='No output')
parser.add_argument('--keep', action='store_true', default=False, help='Keep files after run?')

args = parser.parse_args()

def log(s):
    if args.quiet:
        return
    print("BENCHMARK: {}".format(s))

root = args.path

if root == None:
    root = './'

def bench(**args):
    dirs = []
    endpoint_dirs = []
    times = OrderedDict()
    
    for w in range(0, int(args['width'])):
        line = ["w{}".format(w)]
        for d in range(0, int(args['depth'])):
            line.append("d{}".format(d))
            dirs.append("/".join(line))
    
        endpoint_dirs.append("/".join(line))
    
    t1 = time.time()
    log("Making {} dirs in {}".format(len(dirs), root))
    for d in endpoint_dirs:
        path = root+'/.bench/'+d
        if not os.path.isdir(path):
            log(path)
            os.makedirs(path)
    
    times['makedirs'] = time.time() - t1
    t1 = time.time()
    
    chosen_endpoints = []
    
    log("Making {} files each weighing {}kb in dirs".format(args['files'], args['file_size_bytes']))
    for fnum in range(0, int(args['files'])):
        which = random.choice(endpoint_dirs)
        path = root+'/.bench/'+which
        with open(path+'/file{}.dat'.format(fnum), 'wb') as fh:
            fh.write(os.urandom(int(args['file_size_bytes'])))
            
        chosen_endpoints.append(which)

    times['makefiles'] = time.time() - t1
    t1 = time.time()
    
    for d in chosen_endpoints:
        path = root+'/.bench/'+d
        files = []
        for f in os.listdir(path):
            files.append(f)
        log(d)
        log(files)

    times['listfiles'] = time.time() - t1
            
    if not args['keep']:
        t1 = time.time()
        log("Deleting {} dirs in {}".format(len(dirs), root))
        shutil.rmtree(root+'/.bench/')

        times['delfiles'] = time.time() - t1

    times_int = OrderedDict()
    
    for k,v in times.items():
        vint = float(int(v * 1000))/1000
        times_int[k] = vint

    return times_int


args_dict = vars(args)

width = int(args.width)

for run in range(0, int(args.runs)):
    args_dict['width'] = width*((run+1)*int(args.run_step))
    args_dict['depth'] = int(args.depth)
    
    times = bench(**args_dict)
    times['width'] = args_dict['width']
    times['depth'] = args_dict['depth']
    times['run'] = run
    
    print json.dumps(times, indent=4)
