import os
import time
import sys
import random
import subprocess
import base64
from avro import schema, datafile, io


def process_file(afile, output_path):
    rec_reader = io.DatumReader()
    df_reader = datafile.DataFileReader(open(afile),rec_reader)
    for record in df_reader:
        basename = os.path.basename(record['file_path'])
        dirname = os.path.dirname(record['file_path'])
        x = output_path + dirname 
        x = x.replace('//','/') 
        c = ['mkdir', '-p', x]
        subprocess.call(c)
        fpath = x + '/' + basename
        print fpath
        with open(fpath, 'w') as f:
            b64 = base64.b64decode(record['content'])
            f.write(b64)
            f.close()
       

process_file(sys.argv[1], sys.argv[2])
