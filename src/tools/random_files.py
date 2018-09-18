from os import path, listdir, makedirs
from random import sample
from sys import argv
from shutil import copyfile

# get command line arguments
src_dir = argv[1]
dst_dir = argv[2]
count = int(argv[3])

# safety checks
if not path.exists(src_dir):
    exit(-1)
if len(listdir(src_dir)) == 0:
    exit(-1)
if not path.exists(dst_dir):
    makedirs(dst_dir)

files = listdir(src_dir)

# we can't chose more files than exist
if len(files) < count:
    print('Not enough files!')

random_numbers = sample(range(1, len(files)), count)

# copy the files
for i in range(1, int(count)):
    file_name = files[random_numbers[i]]
    copyfile(src_dir + '/' + file_name,
             dst_dir + '/' + file_name)
