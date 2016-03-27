#!/usr/bin/env python
# @author: Chalres Wei

import multiprocessing, subprocess
import shlex
import sys


def task(cmd):
    cp = multiprocessing.current_process()
    task_name = 'task: %s (pid: %s)' % (cp.name, cp.pid)

    print 'Run %s ...' % task_name
    
    cmd_process = subprocess.Popen(
        shlex.split(cmd),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    output, _ = cmd_process.communicate()

    print '%s => \n%s' % (task_name, output)

    sys.exit(cmd_process.returncode)


def build_jobs(cmds):
    jobs = []
    for cmd in sys.argv[1:]:
        p = multiprocessing.Process(target=task, name=cmd, args=(cmd, ))
        p.daemon = True
        jobs.append(p)
    return jobs


def start_jobs(jobs):
    for j in jobs:
        j.start()


def wait_jobs(jobs):
    for j in jobs:
        j.join()


def get_jobs_results(jobs):
    exitcode = 0
    for j in jobs:
        task_name = 'task: %s (pid: %s)' % (j.name, j.pid)
        result = 'OK' if j.exitcode == 0 else 'FAILED'

        if j.exitcode != 0: exitcode = 255
        print '%s [%s]' % (task_name, result)

    return exitcode


if __name__=='__main__':
    jobs = build_jobs(sys.argv[1:])
    start_jobs(jobs)
    wait_jobs(jobs)

    print '--- All tasks finished ---'
    sys.exit(get_jobs_results(jobs))
