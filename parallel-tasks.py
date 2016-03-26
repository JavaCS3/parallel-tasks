#!/usr/bin/env python
import multiprocessing, subprocess
import shlex
import os, sys


def task(cmd):
    cp = multiprocessing.current_process()
    print 'Run task: %s (pid: %s)...' % (cmd, cp.pid)
    
    try:
        cmd_process = subprocess.Popen(
            shlex.split(cmd),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        output, _ = cmd_process.communicate()
        print '(pid: %s)\n' % cp.pid, output

    except Exception, e:
        raise


if __name__=='__main__':
    jobs = []

    for cmd in sys.argv[1:]:
        p = multiprocessing.Process(target=task, name=cmd, args=(cmd, ))
        p.daemon = True
        jobs.append(p)

    for j in jobs:
        j.start()

    for j in jobs:
        j.join()
        print 'task: %s return: %s' % (j.name, j.exitcode)



 