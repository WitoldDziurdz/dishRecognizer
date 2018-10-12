from glob import glob
import os
dirs = glob('*')

os.mkdir("train")
os.mkdir("test")

for dir in dirs:
    os.mkdir("train/" + dir)
    os.mkdir("test/" + dir)
    i = 1
    if os.path.isfile(dir):
        continue
    for file in os.listdir(dir):
        if i <= 100:
            os.rename(dir + "/" + file, "test/" + dir + "/" + file)
        else:
            os.rename(dir + "/" + file, "train/" + dir + "/" + file)
        i = i + 1
        