avro-serializer
===============

This is a python toolkit that let you serialize in parallel lots of small arbitrary files using the avro format.

The toolkit can be used for data ingestion from and edge node, the resulting avro files are automatically ingested into HDFS.

Please note the script is very simple and easy to use (especially for a POC) and the load is spreaded onto multiple cores 
but this is not an alternative for more complex and fully distributed ingestion tools such as flume.

You can edit the file constants to set the max data size in megabytes to be stored in every avro file (MAX_BATCH_SIZE) and the max number of processes to run in parallel (PROCESSES).

In my usecase I used json further up in the pipeline so I decided to encode the file content in base64, a more standard way of encoding binary values in text/json rather than the raw bytes, but feel free to change the schema provided and the code to accommodate your needs.

(useful posts on base64)

http://mail-archives.apache.org/mod_mbox/avro-dev/200906.mbox/%3C444684557.1243962607373.JavaMail.jira@brutus%3E

http://stackoverflow.com/questions/1443158/binary-data-in-json-string-something-better-than-base64

# Features:
- Native files compression in avro (deflated codec)
- Parallel avro file creation with a configurable file size greater that the hdfs block size
- Schema and metadata avro capabilities (you can add your own additional fields to the schema provided)
- Parallel ingestion into hdfs

# Requirements:
- Python 2.7
- Avro 1.7.4 libraries for Python http://avro.apache.org/docs/current/gettingstartedpython.html

# Improvements:
- Improve performance using iterators rather that lists
- Add a proper command-line parsing (optparse)
- Include snappy compression

# How to use it:
find [input_path] -name '*.*' –print | python serializer.py [output_temp_path] [hdfs_path]

find /mydata/ -name '*.*' –print | python serializer.py /tmp/ /tmp/out/
