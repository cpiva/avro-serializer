import os
import re
import sys
import time
import uuid
import base64
import random
import datetime
import mimetypes
import subprocess
import functools
from multiprocessing import Pool
from avro import schema, datafile, io


FILE_PREFIX = 'c'
SCHEMA_FILE = 'schema.avsc'

# define the max data size in megabytes 
# to be stored in every avro file.
MAX_BATCH_SIZE = 1048576 * 200 

# max nr of processes to run in parallel
PROCESSES = 10


def process_files(output_path, hdfs_path, batch):
    """Process all files in batch a produce an avro file. """
    now = datetime.datetime.now()
    ts = now.strftime("%Y-%m-%d-%H-%M-%S-%f")
    output_filename = FILE_PREFIX + "-" + ts + '.avro'
    print "* creating new avro file: " + output_filename
    xschema = schema.parse(open(SCHEMA_FILE).read())
    rec_writer = io.DatumWriter(xschema)
    df_writer = datafile.DataFileWriter(
                open(output_path + output_filename, 'wb'),
                rec_writer,
                writers_schema = xschema,
                codec = 'deflate')

    for file_path in batch:
        bytes = read_binary(file_path)
        content = base64.b64encode(bytes)
        data = {}
        data['file_path'] = file_path
        data['content'] = content
        df_writer.append(data)
    
    df_writer.close()
    time.sleep(1)
    hdfs_put(output_path + output_filename, hdfs_path)


def get_batches(files):
    """Compute the batches using max content size. """
    totsize = 0
    batches = list()
    batch = list()
    for filepath in files:
        filesize = os.path.getsize(filepath)
        totsize += filesize
        batch.append(filepath)
        if totsize >= MAX_BATCH_SIZE:
            batches.append(batch)
            batch = list()
            totsize = 0
            print "batches:", len(batches)

    if len(batch):
        batches.append(batch)
        print "batches:", len(batches)
    
    return batches


def hdfs_put(path, hdfs_path):
    print "* uploading to hdfs:", path, hdfs_path
    cmd = ['python', 'hdfs_put.py', path, hdfs_path]
    res = subprocess.Popen(cmd)
    return


def read_binary(filepath):
    f = open(filepath, "rb")
    return f.read()


def read_stdin(data):
    paths = list()
    for item in data:
        path = item.replace('\n', '')
        if not os.path.isdir(path):
            paths.append(path)
    return paths


def main(output_path, hdfs_path):
    output_path += "/"
    output_path = output_path.replace('//','/')
    hdfs_path += "/"
    hdfs_path = hdfs_path.replace('//','/')
    paths = read_stdin(sys.stdin)
    batches = get_batches(paths)
    print "nr of batches: " + str(len(batches)) 
    
    pool = Pool(processes=PROCESSES)  	
    ans = pool.map(functools.partial(process_files, output_path, hdfs_path), batches)        
     

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
