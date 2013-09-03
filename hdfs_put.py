import sys
import time
import subprocess
import multiprocessing

def worker(local_path, hdfs_path):
    time.sleep(1)
    cmd = ['hadoop', 'fs', '-put', local_path, hdfs_path]
    res = subprocess.call(cmd)
    if res == 0:
        cmd = ['rm', local_path]
        res = subprocess.call(cmd)
    return

if __name__ == '__main__':
    jobs = []
    local_path = sys.argv[1]
    hdfs_path = sys.argv[2]
    args = (local_path, hdfs_path)
    p = multiprocessing.Process(target=worker, args=args)
    jobs.append(p)
    p.start()
