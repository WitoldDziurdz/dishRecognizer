import glob
import hashlib

dir = "PUT PATH HERE"

filenames = glob.glob(dir)

for filename1 in filenames:
    for filename2 in filenames:
        if filename1 == filename2:
            continue
        else:
            hash1 = ''
            hash2 = ''
            with open(filename1, 'rb') as inputfile:
                data = inputfile.read()
                hash1 = hashlib.md5(data)
            with open(filename2, 'rb') as inputfile:
                data = inputfile.read()
                hash2 = hashlib.md5(data)
            if hash1 == hash2:
                print(filename1)